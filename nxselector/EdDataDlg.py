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
## \file EdDataDlg.py
# editable data dialog

"""  editable data dialog """

import json

from PyQt4.QtCore import (SIGNAL, QString, Qt)
from PyQt4.QtGui import ( QMessageBox,
                          QDialog)

from .ui.ui_eddatadlg import Ui_EdDataDlg

import logging
logger = logging.getLogger(__name__)

## main window class
class EdDataDlg(QDialog):

    ## constructor
    # \param parent parent widget
    def __init__(self, parent=None):
        super(EdDataDlg, self).__init__(parent)
        self.simple = False
        self.name = ''
        self.value = ''
        self.isString = True
        self.ui = Ui_EdDataDlg()

    def createGUI(self):

        self.ui.setupUi(self) 
        if self.simple:
            self.ui.stringCheckBox.hide()
        else:    
            self.isString = isinstance(self.value, 
                                       (str, unicode, QString))
        self.ui.stringCheckBox.setChecked(self.isString)
        self.ui.nameLineEdit.setText(QString(self.name))
        self.ui.valueTextEdit.setText(QString(str(self.value)))

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), 
                     self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), 
                     self.reject)

    def accept(self):
        self.name = unicode(self.ui.nameLineEdit.text())
        self.isString = self.ui.stringCheckBox.isChecked()
        self.value = unicode(self.ui.valueTextEdit.toPlainText())
        if not self.isString and not self.simple:
            try:
                self.value = json.loads(self.value)
            except:
                pass
            
        if not self.name:
            QMessageBox.warning(self, "Wrong Data", "Empty data name" )
            self.ui.nameLineEdit.setFocus()
            return
        QDialog.accept(self)