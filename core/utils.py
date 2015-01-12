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

from PyQt4.QtGui import QColor
from qgis.core import QgsVectorLayer, QgsFeature, QgsMapLayerRegistry, QgsMapLayer

# global variables
layerName = "gebouw" 
adresLayerName = "verblijfsobject" 
editLayerName = "fund_administratief"
geomLayerName = "fund_panden_qgis"
featureRubberColor = QColor(255, 255, 0)
featureRubberSize = 6
atrDefaults = {u'pand_id': 0000L, u'onderzocht': u'f', u'hersteld': u'f', u'kwaliteitsklasse': u'0', u'id': 1L}

def getVectorLayerByName(layerName):
    layerMap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layerMap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.originalName() == layerName:
            if layer.isValid():
                return layer
            else:
                return None

def toBoolean(bool_str):
    """Parse the string and return the boolean value encoded or raise an exception"""
    if isinstance(bool_str, basestring) and bool_str: 
        if bool_str.lower() in ['true', 't', '1', 'ja', 'j']: return True
        elif bool_str.lower() in ['false', 'f', '0', 'nee', 'n']: return False

    #if here we couldn't parse it
    raise ValueError("%s is no recognized as a boolean value" % bool_str)
