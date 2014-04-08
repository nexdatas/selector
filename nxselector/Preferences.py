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
## \file Preferences.py
# preferences tab 

""" preferences tab """

import os
import PyTango
import json

import logging
logger = logging.getLogger(__name__)

from .Views import TableView, CheckerView, RadioView, ButtonView

from PyQt4.QtCore import (
    SIGNAL, QSettings, Qt, QVariant, SIGNAL, QString)

from PyQt4.QtGui import (QMessageBox, QCompleter)
import PyTango

## main window class
class Preferences(object):

    ## constructor
    # \param settings frame settings
    def __init__(self, ui, state = None):
        self.ui = ui
        self.state = state


        # frames/columns/groups
        self.frameshelp = [
            QString('[[[["Counters1", 0], ["Counters2", 2]], [["VCounters", 3]]],'
                + '[[["MCAs", 1], ["SCAs", 4]]], [[["Misc", 5] ]]]'), 
            QString('[[[["My Controllers", 0]]],[[["My Components", 1]]]]'), 
            QString('')]
        self.mgroupshelp = [
            QString('{"2":[["ct01", 0], ["ct02",0]], "5":[["appscan", 1]]}'), 
            QString('')]
        self.serverhelp = [
            QString(self.state.server)]
        
        self.mgroups = str(self.mgroupshelp[0])
        self.frames = str(self.frameshelp[0])

        self.views = {
            "CheckBoxes":CheckerView, 
            "Tables":TableView, 
            "RadioButtons":RadioView,
            "Buttons":ButtonView}

        self.maxHelp = 10

    def connectSignals(self):
        self.ui.preferences.disconnect(
            self.ui.devSettingsLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_devSettingsLineEdit_editingFinished)

        self.ui.preferences.disconnect(
            self.ui.groupLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_groupLineEdit_editingFinished)

        self.ui.preferences.disconnect(
            self.ui.frameLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_frameLineEdit_editingFinished)

        self.ui.preferences.connect(
            self.ui.frameLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_frameLineEdit_editingFinished)

        self.ui.preferences.connect(
            self.ui.groupLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_groupLineEdit_editingFinished)

        self.ui.preferences.connect(
            self.ui.devSettingsLineEdit,
            SIGNAL("editingFinished()"), 
            self.on_devSettingsLineEdit_editingFinished)

       
    def reset(self):
        if self.ui.viewComboBox.count() != len(self.views.keys()):
            self.ui.viewComboBox.clear()
            self.ui.viewComboBox.addItems(sorted(self.views.keys()))
        completer = QCompleter(self.mgroupshelp, self.ui.preferences)
        self.ui.groupLineEdit.setCompleter(completer)
        completer = QCompleter(self.serverhelp, self.ui.preferences)
        self.ui.devSettingsLineEdit.setCompleter(completer) 
        completer = QCompleter(self.frameshelp, self.ui.preferences)
        self.ui.frameLineEdit.setCompleter(completer)
        self.updateForm()
        self.connectSignals()

    def on_devSettingsLineEdit_editingFinished(self):
        server = str(self.ui.devSettingsLineEdit.text())
        if server != self.state.server or True:
            try:
                dp = PyTango.DeviceProxy(server)
                if dp.info().dev_class == 'NXSRecSelector':
                    self.state.server = str(server)
                    qstring = QString(server)
                    if qstring not in self.serverhelp:
                        self.serverhelp.append(server)
                    if self.maxHelp < len(self.serverhelp):
                        self.serverhelp.pop(0)

            except:
                self.reset()
            self.ui.preferences.emit(SIGNAL("serverChanged()"))


    def on_groupLineEdit_editingFinished(self):
        string = str(self.ui.groupLineEdit.text())
        try:
            if not string:
                string = '{}'
            mgroups =  json.loads(string)
            if isinstance(mgroups, dict):
                self.mgroups = string
                qstring = QString(string)
                if qstring not in self.mgroupshelp:
                    self.mgroupshelp.append(string)
                if self.maxHelp < len(self.mgroupshelp):
                    self.mgroupshelp.pop(0)
                self.ui.preferences.emit(
                    SIGNAL("groupsChanged(QString)"),
                    qstring) 
        except:    
            self.reset()


    def on_frameLineEdit_editingFinished(self):
        string = str(self.ui.frameLineEdit.text())
        try:
            if not string:
                string = '[]'
            mframes =  json.loads(string)
            
            if isinstance(mframes, list):
                self.frames = string
                qstring = QString(string)
                if qstring not in self.frameshelp:
                    self.frameshelp.append(string)
                if self.maxHelp < len(self.frameshelp):
                    self.frameshelp.pop(0)
                self.ui.preferences.emit(
                    SIGNAL("framesChanged(QString)"),
                    qstring) 
        except:
            self.reset()



    def updateForm(self):
        self.ui.devSettingsLineEdit.setText(self.state.server)
        self.ui.groupLineEdit.setText(self.mgroups)
        self.ui.frameLineEdit.setText(self.frames)
            

    def apply(self):
        pass