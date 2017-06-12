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
from PyQt4.QtCore import Qt, pyqtSlot, QVariant, QUrl, QTextStream, QFile
from PyQt4.QtGui import QDockWidget, QMessageBox, QDialog
from qgis.core import QGis, QgsGeometry, QgsMapLayerRegistry, QgsMapLayer, QgsFeature, QgsFeatureRequest, QgsVectorDataProvider, QgsOgcUtils
from qgis.gui import QgsRubberBand, QgsMessageBar

from utils import *
from fieldcombo import *
from bagadres import *
from infoperceeldialog import PerceelinfoDialog
from infobagdialog import InfoBagDialog
from infoverseondialog import InfoVerseonDialog
from ..ui.ui_dockeditor import Ui_DockEditor
# create the dialog for zoom to point

class DockEditorDialog(QtGui.QDockWidget, Ui_DockEditor):
    def __init__(self, iface, mapCanvas):
        self.iface = iface
        QtGui.QDockWidget.__init__(self)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self)

        self.mapCanvas = mapCanvas

        # rubber bands
        self.featureRubber = QgsRubberBand(self.mapCanvas, False)
        self.updateFeatureRubber()

        # Gui defaults
        self.kwaliteitsklasseCombo.setVisible(False)
        self.onderzochtJaarSpinBox.setVisible(False)
        self.hersteldJaarSpinBox.setVisible(False)
        self.kwaliteitsklasseLabel.setVisible(False)
        self.monitoringObjTekst.setVisible(False)

        # GUI signals connection
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.applySave)
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Abort).clicked.connect(self.applyCancel)
        self.deleteButton.clicked.connect(self.applyDelete)
        self.newPandButton.clicked.connect(self.applyNewPand)
        self.idButton.clicked.connect(self.zoomToFeature)
        self.adresLinkButton.clicked.connect(self.showVerblijfsObj)
        self.verseonLinkButton.clicked.connect(self.getVerseonInfo)
        self.lkiLinkButton.clicked.connect(self.showLkiInfo)

        # force Dutch for QDialogButtonBox
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Save).setText("Opslaan")
        self.actionButtonBox.button(QtGui.QDialogButtonBox.Abort).setText("Annuleer");

        # enable save button when value changes
        self.bezitCombo.currentIndexChanged.connect(self.actionButtonBoxEnable)
        self.kwaliteitsklasseCombo.currentIndexChanged.connect(self.actionButtonBoxEnable)
        self.onderzochtCheckBox.stateChanged.connect(self.actionButtonBoxEnable)
        self.onderzochtJaarSpinBox.valueChanged.connect(self.actionButtonBoxEnable)
        self.hersteldCheckBox.stateChanged.connect(self.actionButtonBoxEnable)
        self.hersteldJaarSpinBox.valueChanged.connect(self.actionButtonBoxEnable)
        self.projectCombo.editTextChanged.connect(self.actionButtonBoxEnable)
        self.richtlijnCombo.editTextChanged.connect(self.actionButtonBoxEnable)
        self.handhavingCheckBox.stateChanged.connect(self.actionButtonBoxEnable)
        self.typefundCombo.editTextChanged.connect(self.actionButtonBoxEnable)
        self.paallengteSpinBox.valueChanged.connect(self.actionButtonBoxEnable)
        self.houtsoortCombo.editTextChanged.connect(self.actionButtonBoxEnable)
        self.dekkingSpinBox.valueChanged.connect(self.actionButtonBoxEnable)
        self.droogstandCheckBox.stateChanged.connect(self.actionButtonBoxEnable)
        self.opmerkingText.textChanged.connect(self.actionButtonBoxEnable)

        self.setVisible(False)

    def showEvent(self, e):

        self.newGroupBox.hide()
        self.editGroupBox.hide()
        if (getVectorLayerByName(editLayerName) == None):
            self.errorFrame.show()
        else:
            self.errorFrame.hide()

        self.editLayer = getVectorLayerByName(editLayerName)
        self.adresLayer = getVectorLayerByName(adresLayerName)
        self.geomLayer = getVectorLayerByName(geomLayerName)
        self.editFeature = None
        self.updateCombos()

    def closeEvent(self, e):

        e.ignore()
        self.featureRubber.reset()
        self.hide()

    def zoomToFeature(self):
        box = self.selectedFeature.geometry().buffer(20, 4).boundingBox()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def updateCombos(self):

        if (self.editLayer):
            FieldCombo(self.bezitCombo, self.editLayer, initField="bezit")
            FieldCombo(self.kwaliteitsklasseCombo, self.editLayer, initField="kwaliteitsklasse")
            FieldCombo(self.projectCombo, self.editLayer, initField="project")
            FieldCombo(self.richtlijnCombo, self.editLayer, initField="richtlijn")
            FieldCombo(self.typefundCombo, self.editLayer, initField="funderingtype")
            FieldCombo(self.houtsoortCombo, self.editLayer, initField="houtsoort")

    def actionButtonBoxEnable(self):
        self.actionButtonBox.setDisabled(False)

    def featureSelected(self, layer, feature):
        self.layer = layer
        self.selectedFeature = feature
        initialGeometry = QgsGeometry(feature.geometry())

        self.featureRubber.reset()
        self.featureRubber.setToGeometry(initialGeometry, layer)
        self.updateGui(feature)

    def updateGui(self, feature):
        # The important part: get the feature iterator with an expression
        request = QgsFeatureRequest().setFilterExpression ( u'"pand_id" = \'' + unicode(feature['gebouwnummer']) + '\'' )
        request.setFlags( QgsFeatureRequest.NoGeometry )
        features = self.geomLayer.getFeatures( request )

        atr = None
        fields = self.geomLayer.pendingFields()
        field_names = [field.name() for field in fields]
        for elem in features:
            self.editFeature = elem
            atr = dict(zip(field_names, elem.attributes()))

        if atr is not None:
            atr = {i:j for i,j in atr.items() if j }
            self.newGroupBox.hide()
            self.editGroupBox.show()
            self.verwijderWidget.show()
            self.showValues(feature, atr)
            self.actionButtonBox.setDisabled(True)

        else:
            self.newGroupBox.show()
            self.editGroupBox.hide()
            self.verwijderWidget.hide()

            self.editFeature = None
            self.statusNieuwLabel.setText(unicode(feature['status']))
            self.pandidLabel.setText(unicode(feature['gebouwnummer']))

    def showValues(self, feature, atr):

        self.deleteCheckBox.setChecked(False)

        self.idText.setText(unicode(atr.get("pand_id", "")))
        if (feature['vboj_count'] == 1):
            self.adresLinkButton.setText(BagadresString().request(unicode(feature['gebouwnummer'])))
        else:
            self.adresLinkButton.setText("Pand bevat " + unicode(feature['vboj_count']) + " adres(sen)")

        self.setComboTekst(self.bezitCombo, atr.get("bezit", ""))

        if (atr.get("onderzocht", "")=="t"):
            self.onderzochtCheckBox.setChecked(True)
            self.onderzochtJaarSpinBox.setValue(atr.get("onderzocht_jaar", ""))
        else:
            self.onderzochtCheckBox.setChecked(False)

        self.setComboTekst(self.kwaliteitsklasseCombo, atr.get("kwaliteitsklasse", ""))

        if (atr.get("hersteld", "")=="t"):
            self.hersteldCheckBox.setChecked(True)
            self.hersteldJaarSpinBox.setValue(atr.get("hersteld_jaar", ""))
        else:
            self.hersteldCheckBox.setChecked(False)

        self.setComboTekst(self.projectCombo, atr.get("project", ""))
        self.setComboTekst(self.richtlijnCombo, atr.get("richtlijn", ""))
        
        self.handhavingCheckBox.setChecked(toBoolean(atr.get("fumon_monitoring", "f")))
        self.monitoringObjTekst.setText(atr.get("fumon_objectcode", ""))

        self.setComboTekst(self.typefundCombo, atr.get("funderingtype", ""))
        self.paallengteSpinBox.setValue(atr.get("paallengte", 0))
        self.setComboTekst(self.houtsoortCombo, atr.get("houtsoort", ""))
        self.dekkingSpinBox.setValue(atr.get("dekking", 0))
        self.droogstandCheckBox.setChecked(toBoolean(atr.get("droogstand", "f")))

        self.opmerkingText.setPlainText(atr.get("opmerking", ""))      

        # set texts in UI
        featureStatus = unicode(feature['status'])
        featureBj = unicode(feature['bouwjaar'])

        self.statusText.setText(featureStatus)
        self.bouwjaarText.setText(featureBj)

    def showVerblijfsObj(self):
        feature = self.selectedFeature
        gebouwnummer = unicode(feature['gebouwnummer'])
        InfoBagDialog(gebouwnummer, self.iface)

    def getVerseonInfo(self):
        feature = self.selectedFeature
        gebouwnummer = unicode(feature['gebouwnummer'])
        InfoVerseonDialog(gebouwnummer, self.iface)

    def showLkiInfo(self):
        feature = self.selectedFeature
        wkt = feature.geometry().pointOnSurface().exportToWkt()
        PerceelinfoDialog(wkt, self.iface)

    def setComboTekst(self, combo, value):
        idx = combo.findText(value)
        combo.setCurrentIndex(idx)

    def updateFeatureRubber(self):
        self.featureRubber.setColor(featureRubberColor)
        self.featureRubber.setWidth(featureRubberSize)
        self.featureRubber.setBrushStyle(Qt.NoBrush)
        self.mapCanvas.refresh()

    def applySave(self):

        if not self.editLayer.isEditable():
            self.editLayer.startEditing()

        layer = self.editLayer
        layer.beginEditCommand("Funderingsgegevens")

        try:

            if (self.editFeature == None):
                idx = layer.pendingFields().indexFromName("id")
                nextId = layer.maximumValue(idx)
                feat = QgsFeature()
                feat.setFields(layer.pendingFields(), True)
                feat.setAttribute(layer.fieldNameIndex( "pand_id" ), self.pandidLabel.text())
                feat.setAttribute(layer.fieldNameIndex( "id" ), nextId + 1)
                layer.addFeature(feat, False)
                self.editFeature = feat

            fid = self.editFeature.id()

            layer.changeAttributeValue(fid, layer.fieldNameIndex( "pand_id" ), self.idText.text())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "bezit" ), self.bezitCombo.currentText())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "onderzocht" ), self.onderzochtCheckBox.isChecked())
            if (self.onderzochtCheckBox.isChecked()):
                layer.changeAttributeValue(fid, layer.fieldNameIndex( "onderzocht_jaar" ), self.onderzochtJaarSpinBox.value())
            else:
                layer.changeAttributeValue(fid, layer.fieldNameIndex( "onderzocht_jaar" ), None)
                
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "kwaliteitsklasse" ), self.kwaliteitsklasseCombo.currentText())

            layer.changeAttributeValue(fid, layer.fieldNameIndex( "hersteld" ), self.hersteldCheckBox.isChecked())
            if (self.hersteldCheckBox.isChecked()):
                layer.changeAttributeValue(fid, layer.fieldNameIndex( "hersteld_jaar" ), self.hersteldJaarSpinBox.value())
            else:
                layer.changeAttributeValue(fid, layer.fieldNameIndex( "hersteld_jaar" ), None)

            layer.changeAttributeValue(fid, layer.fieldNameIndex( "project" ), self.projectCombo.currentText())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "richtlijn" ), self.richtlijnCombo.currentText())

            layer.changeAttributeValue(fid, layer.fieldNameIndex( "funderingtype" ), self.typefundCombo.currentText())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "paallengte" ), self.paallengteSpinBox.value())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "houtsoort" ), self.houtsoortCombo.currentText())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "dekking" ), self.dekkingSpinBox.value())
            layer.changeAttributeValue(fid, layer.fieldNameIndex( "droogstand" ), self.droogstandCheckBox.isChecked())

            layer.changeAttributeValue(fid, layer.fieldNameIndex( "opmerking" ), self.opmerkingText.toPlainText())
        except Exception, e:
            raise e
            layer.destroyEditCommand()
            self.iface.messageBar().pushMessage("Funderingsherstel", "Er is wat misgegaan tijdens het opslaan van dit BAG object!", level=QgsMessageBar.CRITICAL)
        else:
            layer.endEditCommand()
            layer.commitChanges()
            self.geomLayer.triggerRepaint()
            self.iface.messageBar().pushMessage("Funderingsherstel", "BAG object " + self.idText.text() + " is opgeslagen...", level=QgsMessageBar.INFO)

        self.updateCombos()
        self.updateGui(self.selectedFeature)

    def applyCancel(self):
        self.updateGui(self.selectedFeature)

    def applyDelete(self):

        layer = self.editLayer
        layer.startEditing()
        fid = self.editFeature.id()
        layer.deleteFeature(fid)
        layer.commitChanges()
        self.layer.triggerRepaint()
        self.geomLayer.triggerRepaint()
        self.updateGui(self.selectedFeature)

    def applyNewPand(self):

        self.newGroupBox.hide()
        self.editGroupBox.show()

        atr = atrDefaults
        atr["pand_id"] = self.pandidLabel.text()
        atr["kwaliteitsklasse"] = "Onbekend"

        self.showValues(self.selectedFeature, atrDefaults)
        self.actionButtonBox.setDisabled(False)
