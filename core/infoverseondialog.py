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
from PyQt4.QtGui import QDialog, QTableWidgetItem, QDesktopServices
from qgis.core import QGis
from qgis.gui import QgsMessageBar
import json

from ..ui.ui_popup import Ui_Info

class InfoVerseonDialog(QDialog, Ui_Info):
    def __init__(self, gebouwnummer, iface, parent=None):
        super(InfoVerseonDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Verseon documenten')
        self.label.setText('Dubbelklik om link te openen')
        
        self.tableWidget.itemDoubleClicked.connect(self.showItem)
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Close).setText("Sluiten")

        self.basewfs = "http://map16z/geoserver/wfs?request=GetFeature&version=2.0.0&outputFormat=JSON"
        self.iface = iface
        self.manager = QNetworkAccessManager(self)
        self.gebouwnummer = gebouwnummer
        self.getInfo(self.gebouwnummer)
        self.exec_()

    def getInfo(self, gebouwnummer):
        qurl = QUrl.fromUserInput(self.basewfs)
        qurl.addQueryItem('typeName', 'geo:fund_verseon')
        qurl.addQueryItem('filter', "<PropertyIsEqualTo><PropertyName>gebouwnummer</PropertyName><Literal>" + unicode(gebouwnummer) + "</Literal></PropertyIsEqualTo>")
        request = QNetworkRequest(qurl)
        reply = self.manager.get(request)
        reply.finished.connect(self.handleInfo)

    def handleInfo(self):
        reply = self.sender()
        error = reply.error()
        if error != QNetworkReply.NoError:
            self.iface.messageBar().pushMessage(reply.errorString(), level=QgsMessageBar.WARNING)
            reply.deleteLater()
            reply = None
        else:
            response_text = reply.readAll().data()
            data = json.loads(response_text)
            count = data['totalFeatures']
            if (count == 0):
                self.tableWidget.clear()
                self.tableWidget.setColumnCount(1);
                self.tableWidget.setRowCount(1);
                text = QTableWidgetItem('Geen documenten gevonden')
                self.tableWidget.setItem(0,0,text)
                self.tableWidget.resizeColumnToContents(0)
            else:    
                self.tableWidget.clear()
                self.tableWidget.setColumnCount(3);
                self.tableWidget.setRowCount(count);
                features = data['features']
                for idx, feature in enumerate(features):
                    text1 = QTableWidgetItem(feature['properties']['dossier'])
                    text1.setToolTip(feature['properties']['verseonlink'])

                    text2 = QTableWidgetItem(feature['properties']['zaakomschrijving'])
                    text2.setToolTip(feature['properties']['zaakomschrijving'])
                    
                    value = QTableWidgetItem(feature['properties']['verseonlink'])
                    self.tableWidget.setItem(idx,0,text1)
                    self.tableWidget.setItem(idx,1,text2)
                    self.tableWidget.setItem(idx,2,value)
                
                self.tableWidget.setColumnHidden(2, True)
                self.tableWidget.resizeColumnToContents(0)
                self.tableWidget.resizeColumnToContents(1)

    def showItem(self, item):
        row = item.row()
        qurl = QUrl.fromUserInput(self.tableWidget.item(row, 2).text())
        QDesktopServices.openUrl(qurl)