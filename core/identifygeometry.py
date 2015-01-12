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

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QPixmap, QCursor
from qgis.core import QgsVectorLayer, QgsFeature, QgsMapLayerRegistry, QgsMapLayer
from qgis.gui import QgsMapToolIdentify

from cursor import Cursor
from utils import *

class IdentifyGeometry(QgsMapToolIdentify):
    geomIdentified = pyqtSignal(QgsVectorLayer, QgsFeature)

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolIdentify.__init__(self, canvas)
        self.setCursor(QCursor(QPixmap(Cursor), 1, 6))

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, mouseEvent):

        if mouseEvent.button() == QtCore.Qt.RightButton:
            print("release clicked right")

        layerA = getVectorLayerByName(layerName)
        try:
            results = self.identify(mouseEvent.x(), mouseEvent.y(), [layerA], self.TopDownStopAtFirst)
        except:
            results = self.identify(mouseEvent.x(), mouseEvent.y(), self.TopDownStopAtFirst, self.VectorLayer)
        if len(results) > 0:
            self.geomIdentified.emit(results[0].mLayer, QgsFeature(results[0].mFeature))



    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True