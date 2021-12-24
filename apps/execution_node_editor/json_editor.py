from json.decoder import JSONDecodeError
from subprocess import call
from typing import Dict
from PyQt5 import QtCore
from PyQt5 import QtGui
from pyqode.core.api import syntax_highlighter
from pyqode.core.api.decoration import TextDecoration
from qtpy.QtCore import Qt
from PyQtJsonModel import QJsonModel

from pyqode.qt import QtWidgets
from pyqode.json.widgets import JSONCodeEdit

from PyQt5.QtWidgets import QAbstractItemView, QTreeView

import json 

def countLines(text):
    return len(text.split('\n'))

class JsonEditor(QtWidgets.QDockWidget):
    def __init__(self):
        super(JsonEditor, self).__init__()
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)
        self.tree = QTreeView(self)
        self.setWidget(self.tree)
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        self.setWindowTitle("Node Settings")
        self.callback = None
        self.tree.setStyleSheet('QTreeView { alternate-background-color: #f7f7f7; font-family: Roboto; font-size: 12pt;} QTreeView::item { height: 25px; }')
        self.tree.setAlternatingRowColors(True)
        self.tree.setEditTriggers(QAbstractItemView.AllEditTriggers)

    def update(self, json_dict, callback, active):
        if active:
            self.setWidget(self.tree)
            self.json_model = QJsonModel(json_data=json_dict)
            self.json_model.dataChanged.connect(self.apply_change)
            self.tree.setModel(self.json_model)
            self.callback = callback

        else:
            self.setWidget(None)
            #self.json_model = None
            self.callback = None

    def apply_change(self):
        had_error = True
        json_dict = {}
        try:
            json_dict = self.json_model.as_dict
            had_error = False
        except:
            had_error = True

        if had_error == False and self.callback is not None:
            print('Apply new settings to node')
            print(json_dict)
            self.callback(json_dict)
