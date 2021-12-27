from json.decoder import JSONDecodeError
from subprocess import call
from typing import Dict
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from qtpy.QtCore import Qt
from PyQtJsonModel import QJsonModel

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
        self.setWindowTitle("NODE SETTINGS")
        self.setFont(QtGui.QFont('Roboto', 10))
        self.callback = None
        self.tree.setStyleSheet('QTreeView { '
        'alternate-background-color: #252b3b; '
        'selection-background-color: #1a4b61;' 
        'font-family: Roboto; '
        'font-size: 12pt; '
        'color: #a0a9b8'
        '}'
        'QTreeView::item { height: 25px; }'
        'QTreeView::item {'
        '    selection-color: #ffffff;'
        '}'
        'QTreeView::item:hover {'
        '        color: #ffffff;'
        '}'
        )
        self.tree.setAlternatingRowColors(True)
        self.tree.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tree.header().setStyleSheet(
            'QHeaderView::section {'                          
            'color: #a0a9b8;' 
            'font-family: Roboto; font-size: 12pt;'
                                        
            #'padding: 0px;'                               
            'height: 25px;'                                
            #'border: 0px solid #2c3748;'                  
            #'border-left:1px;'                            
            #'border-right:1px;'                           
            'background: #151a24;'                        
        '}')

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
