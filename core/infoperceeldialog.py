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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QVariant, QUrl
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from PyQt4.QtGui import QDialog
from qgis.core import QGis
from qgis.gui import QgsMessageBar
import json

from ..ui.ui_perceelinfo import Ui_Perceelinfo

class PerceelinfoDialog(QDialog, Ui_Perceelinfo):
    def __init__(self, wkt, iface, parent=None):
        super(PerceelinfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Kadastrale informatie')
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Close).setText("Sluiten")

        self.basewfs = "http://map16z/geoserver/wfs?request=GetFeature&version=2.0.0&outputFormat=JSON"
        self.iface = iface
        self.manager = QNetworkAccessManager(self)
        self.wkt = wkt
        self.getLkiInfo(self.wkt)
        self.exec_()

    def showEvent(self, e):
        super(PerceelinfoDialog, self).showEvent(e)

    def closeEvent(self, e):
        super(PerceelinfoDialog, self).closeEvent(e)

    def getLkiInfo(self, wkt):
        #geom_ogr = ogr.CreateGeometryFromWkt(wkt)
        #gml = geom_wkt.ExportToGML()
        qurl = QUrl.fromUserInput(self.basewfs)
        qurl.addQueryItem('typeName', 'geo:brk_perceel')
        qurl.addQueryItem('cql_filter', "CONTAINS(geom," + wkt + ")")
        request = QNetworkRequest(qurl)
        reply = self.manager.get(request)
        reply.finished.connect(self.handleLkiInfo)

    def handleLkiInfo(self):
        reply = self.sender()
        error = reply.error()
        if error != QNetworkReply.NoError:
            self.iface.messageBar().pushMessage(reply.errorString(), level=QgsMessageBar.WARNING)
            reply.deleteLater()
            reply = None
            self.close()
        else:
            response_text = reply.readAll().data()
            perceeldata = json.loads(response_text)
            totalFeatures = perceeldata['totalFeatures']

            properties = perceeldata['features'][0]['properties']
            self.perceelText.setText(unicode(properties['aanduiding']))
            self.oppervlakteText.setText(unicode(properties['kadastralegrootte']))

            self.getAkrInfo(unicode(properties['id']))

    def getAkrInfo(self, id):
        qurl = QUrl.fromUserInput(self.basewfs)
        qurl.addQueryItem('typeName', 'geo:brk_zak_recht')
        qurl.addQueryItem('cql_filter', "rust_op_kadastraalobject_id='" + id + "'")
        print qurl
        request = QNetworkRequest(qurl)
        reply = self.manager.get(request)
        reply.finished.connect(self.handleAkrInfo)

    def handleAkrInfo(self):
        reply = self.sender()
        error = reply.error()
        if error != QNetworkReply.NoError:
            self.listWidget.addItems(['Fout bij het ophalen van AKR info!'])
        else:
            response_text = reply.readAll().data()
            data = json.loads(response_text)
            features = data['features']
            ownerList = []
            for feature in features:
                properties = feature['properties']
                text = properties.get('naam').strip() + ' ' if properties['naam'] != None else u''
                text += ' - ' + properties.get('omschrijving').strip() + ' ' if properties['omschrijving'] != None else u''
                text += ' - '
                text += properties.get('teller').strip() + '/' + properties.get('noemer').strip() if properties['noemer'] != None else u''
                ownerList.append(text)

            self.listWidget.addItems(ownerList)

