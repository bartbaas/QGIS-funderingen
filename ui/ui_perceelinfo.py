# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_perceelinfo.ui'
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

class Ui_Perceelinfo(object):
    def setupUi(self, Perceelinfo):
        Perceelinfo.setObjectName(_fromUtf8("Perceelinfo"))
        Perceelinfo.resize(374, 321)
        Perceelinfo.setSizeGripEnabled(True)
        self.formLayout = QtGui.QFormLayout(Perceelinfo)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.perceelText = QtGui.QLineEdit(Perceelinfo)
        self.perceelText.setReadOnly(True)
        self.perceelText.setObjectName(_fromUtf8("perceelText"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.perceelText)
        self.label_3 = QtGui.QLabel(Perceelinfo)
        self.label_3.setMinimumSize(QtCore.QSize(100, 0))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(Perceelinfo)
        self.label_4.setMinimumSize(QtCore.QSize(100, 0))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_4)
        self.oppervlakteText = QtGui.QLineEdit(Perceelinfo)
        self.oppervlakteText.setReadOnly(True)
        self.oppervlakteText.setObjectName(_fromUtf8("oppervlakteText"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.oppervlakteText)
        self.label = QtGui.QLabel(Perceelinfo)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.label)
        self.listWidget = QtGui.QListWidget(Perceelinfo)
        self.listWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.listWidget)
        self.actionButtonBox = QtGui.QDialogButtonBox(Perceelinfo)
        self.actionButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.actionButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.actionButtonBox.setObjectName(_fromUtf8("actionButtonBox"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.actionButtonBox)

        self.retranslateUi(Perceelinfo)
        QtCore.QObject.connect(self.actionButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Perceelinfo.reject)
        QtCore.QObject.connect(self.actionButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Perceelinfo.accept)
        QtCore.QMetaObject.connectSlotsByName(Perceelinfo)

    def retranslateUi(self, Perceelinfo):
        Perceelinfo.setWindowTitle(_translate("Perceelinfo", "Dialog", None))
        self.label_3.setText(_translate("Perceelinfo", "Perceel", None))
        self.label_4.setText(_translate("Perceelinfo", "Oppervlakte", None))
        self.label.setText(_translate("Perceelinfo", "Eigenaren", None))
        self.listWidget.setSortingEnabled(True)

