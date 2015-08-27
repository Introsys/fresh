# Form implementation generated from reading ui file 'SplashScreen.ui'
#
# Created: Wed Aug 19 14:38:37 2015
#      by: PyQt4 UI code generator 4.10.4
#
# Please do not generate this file from the original SplashScreen.ui
# or all the changes made to this document will be lost
# The Ui file serves only for making the template UI


import resources_rc
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



# ----------------------------------------------------------------------------------------------
class Ui_WidgetLogo(QtGui.QWidget):
  
  # --------------------------------------------------------------------------
  def __init__(self):
    super(Ui_WidgetLogo, self).__init__()
    self.setupUi(self)
    resources_rc.qInitResources()
  
  # --------------------------------------------------------------------------
  def setupUi(self, WidgetLogo):
    
    WidgetLogo.setObjectName(_fromUtf8("WidgetLogo"))
    WidgetLogo.resize(633, 475)
    
    self.gridLayout = QtGui.QGridLayout(WidgetLogo)
    self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
    
    # ------------------------------------------------------------------
    # Add logo to central widget
    self.l_logo = QtGui.QLabel(WidgetLogo)
    self.l_logo.setText(_fromUtf8(""))
    self.l_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/fresh.png")))
    self.l_logo.setAlignment(QtCore.Qt.AlignCenter)
    self.l_logo.setObjectName(_fromUtf8("l_logo"))    
    self.gridLayout.addWidget(self.l_logo, 0, 0, 1, 1)

    self.retranslateUi(WidgetLogo)
    QtCore.QMetaObject.connectSlotsByName(WidgetLogo)

  
  # --------------------------------------------------------------------------
  def retranslateUi(self, WidgetLogo):
    WidgetLogo.setWindowTitle(_translate("WidgetLogo", "Form", None))
    
    
    
#EOF