#-----------------------------------------------------------
#
# Funderingsherstel is a QGIS plugin to manage foundation data
#
# Copyright    : (C) 2014 Bart Baas
# Email        : b.baas@zaanstad.nl
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import Qt, QObject, QEventLoop, QUrl, QTimer
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
import json

class BagadresString(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.basewfs = "http://geo.zaanstad.nl/geoserver/wfs?request=GetFeature&version=2.0.0&outputFormat=JSON"
        self.manager = QNetworkAccessManager(self)
        self.timer = QTimer()
        self.loop = QEventLoop()
        self.reply = None
        
    def request(self, gebouwnummer):
        qurl = QUrl.fromUserInput(self.basewfs)
        qurl.addQueryItem('typeName', 'geo:bag_verblijfsobject')
        qurl.addQueryItem('filter', "<PropertyIsEqualTo><PropertyName>gebouwnummer</PropertyName><Literal>" + unicode(gebouwnummer) + "</Literal></PropertyIsEqualTo>")
        request = QNetworkRequest(qurl)
        
        self.reply = self.manager.get(request)
        self.reply.finished.connect(self.loop.quit)

        self.timer.start(5000)
        self.loop.exec_()

        if self.timer.isActive():
            self.timer.stop()
            r = self.handleReply()
        else:
            raise Exception("Timeout error.")

        return r

    def handleReply(self):
        reply = self.reply
        response_text = reply.readAll().data()
        data = json.loads(response_text)
        feature = data['features'][0]
        reply.deleteLater()
        return feature['properties']['adres'] + " (" + feature['properties']['gebruik'] + ")"
