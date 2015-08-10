# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_popup.ui'
#
# Created: Mon Aug 10 12:09:51 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Info(object):
    def setupUi(self, Info):
        Info.setObjectName(_fromUtf8("Info"))
        Info.resize(371, 413)
        Info.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Info)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Info)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtGui.QTableWidget(Info)
        self.tableWidget.setFrameShadow(QtGui.QFrame.Plain)
        self.tableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)
        self.actionButtonBox = QtGui.QDialogButtonBox(Info)
        self.actionButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.actionButtonBox.setObjectName(_fromUtf8("actionButtonBox"))
        self.verticalLayout.addWidget(self.actionButtonBox)

        self.retranslateUi(Info)
        QtCore.QObject.connect(self.actionButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Info.reject)
        QtCore.QMetaObject.connectSlotsByName(Info)

    def retranslateUi(self, Info):
        Info.setWindowTitle(_translate("Info", "Dialog", None))
        self.label.setText(_translate("Info", "TextLabel", None))

