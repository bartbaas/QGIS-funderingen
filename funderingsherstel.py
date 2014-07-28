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
from PyQt4.QtCore import QUrl
from PyQt4.QtGui import QAction, QIcon, QDesktopServices

from core.identifygeometry import IdentifyGeometry
from core.dockeditordialog import DockEditorDialog
from core.utils import *

import resources
import os.path

class FunderingGeometryEditor():

    def __init__(self, iface):
        self.iface = iface
        self.mapCanvas = iface.mapCanvas()
        self.mapTool = None
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
   
    def initGui(self):
        # help
        self.helpAction = QAction(QIcon(":/funderingsherstel/icons/help.svg"), "Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: QDesktopServices().openUrl(QUrl("mailto:geo-informatie@zaanstad.nl")))

        # map tool action
        self.mapToolAction = QAction(QIcon(":/funderingsherstel/icons/fundering.svg"),
                                     u"Funderingsherstel", self.iface.mainWindow())
        self.mapToolAction.setCheckable(True)
        self.mapToolAction.triggered.connect(self.setMapTool)

        self.iface.addToolBarIcon(self.mapToolAction)

        # Create the dock (after translation) and keep reference
        self.dock = DockEditorDialog(self.iface, self.mapCanvas)
        self.dock.visibilityChanged.connect(self.unsetMapTool)
        
        # menu
        self.iface.addPluginToMenu("&Funderingsherstel", self.mapToolAction)
        self.iface.addPluginToMenu("&Funderingsherstel", self.helpAction)

    def unload(self):
        self.iface.removePluginMenu("&Funderingsherstel", self.helpAction)
        self.iface.removePluginMenu("&Funderingsherstel", self.mapToolAction)
        self.iface.removeToolBarIcon(self.mapToolAction)

        self.dock.hide()
        self.dock.deleteLater()

    def unsetMapTool(self):
        self.mapToolAction.setChecked( self.dock.isVisible() )

        if (self.mapToolAction.isChecked() is False and self.mapTool is not None):
            self.mapCanvas.unsetMapTool(self.mapTool)

    def setMapTool(self):

        self.dock.errorFrame.hide()

        if self.mapToolAction.isChecked() is False:
            self.dock.close()
        else:
            self.dock.show()
            if (getVectorLayerByName(editLayerName) == None):
                self.dock.errorFrame.show()
            else:
                self.mapTool = IdentifyGeometry(self.mapCanvas)
                self.mapTool.geomIdentified.connect(self.editGeometry)
                self.mapTool.setAction(self.mapToolAction)
                self.mapCanvas.setMapTool(self.mapTool)

    def editGeometry(self, layer, feature):
        self.dock.featureSelected(layer, feature)


