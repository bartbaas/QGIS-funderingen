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

from PyQt4.QtCore import Qt, QObject, pyqtSignal
from qgis.core import QgsVectorLayer

class FieldCombo(QObject):
    fieldChanged = pyqtSignal()

    def __init__(self, widget, vectorLayer, initField=""):
        QObject.__init__(self)
        if not isinstance(vectorLayer, QgsVectorLayer):
            raise NameError("You must provide a VectorLayer.")
        self.widget = widget
        self.layer = vectorLayer
        self.initField = initField
        self.widget.currentIndexChanged.connect(self.currentIndexChanged)
        self.__layerChanged()

    def currentIndexChanged(self, i):
        self.fieldChanged.emit()

    def __layerChanged(self):
        if hasattr(self.initField, '__call__'):
            initField = self.initField()
        else:
            initField = self.initField
        self.widget.clear()
        if self.layer is None:
            return
        for value in self.layer.uniqueValues(self.getFieldIndex(self.initField)):
            if (value):
                self.widget.addItem(value)

    def __layerDeleted(self):
        self.layer = None

    def getFieldIndex(self, fieldName):
        idx = self.layer.pendingFields().indexFromName(fieldName)
        if idx != -1:
            self.widget.setCurrentIndex(idx)
        return idx