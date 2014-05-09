#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2014 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
## \package nxselector nexdatas
## \file LDataDlg.py
# editable data dialog

"""  editable data dialog """

import json

from PyQt4.QtCore import (SIGNAL, QString, Qt)
from PyQt4.QtGui import ( QMessageBox,
                          QDialog)

from .ui.ui_ldatadlg import Ui_LDataDlg

import logging
logger = logging.getLogger(__name__)

## main window class
class LDataDlg(QDialog):

    ## constructor
    # \param parent parent widget
    def __init__(self, parent=None):
        super(LDataDlg, self).__init__(parent)
        self.label = ''
        self.path = ''
        self.shape = None
        self.dtype = ''
        self.link = None
        self.ui = Ui_LDataDlg()
     
    def __linkText(self, value):
        if value == True:
            return "True"
        if value == False:
            return "False"
        return "Default"
        

    def createGUI(self):

        self.ui.setupUi(self) 
        self.ui.labelLineEdit.setText(QString(str(self.label)))
        self.ui.pathLineEdit.setText(QString(str(self.path)))
        if self.shape is None:
            shape = ''
        else:
            shake = self.shape
        self.ui.shapeLineEdit.setText(QString(str(shape)))
        self.ui.typeLineEdit.setText(QString(str(self.dtype)))
   
        cid = self.ui.linkComboBox.findText(QString(self.__linkText(self.link)))
        if cid < 0:
            cid = 0
        self.ui.linkComboBox.setCurrentIndex(cid) 

    def accept(self):
        link = str(self.ui.linkComboBox.currentText())
        if link == "True":
            self.link = True
        elif link == "False":
            self.link = False
        else:
            self.link = None

        self.label = unicode(self.ui.labelLineEdit.text())
        self.path = unicode(self.ui.pathLineEdit.text())
        self.dtype = unicode(self.ui.typeLineEdit.text())
        tshape = unicode(self.ui.shapeLineEdit.text())
        try:
            if not tshape:
                self.shape = None
            else:
                shape = json.load(tshape)
                assert isinstance(shape, list)
                self.shape = shape
        except:
            QMessageBox.warning(self, "Wrong Data", "Wrong structure of Shape" )
            self.ui.shapeLineEdit.setFocus()
            return
            
        self.dtype = unicode(self.ui.typeLineEdit.text())

           
        if not self.label:
            QMessageBox.warning(self, "Wrong Data", "Empty data label" )
            self.ui.labelLineEdit.setFocus()
            return

        QDialog.accept(self)