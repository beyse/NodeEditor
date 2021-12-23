from json.decoder import JSONDecodeError
import os
from subprocess import call
from typing import Dict
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush, QColor, QCursor
from pyqode.core.api import syntax_highlighter
from pyqode.core.api.decoration import TextDecoration
from qtpy.QtCore import Qt
import re

from pyqode.qt import QtWidgets
from pyqode.json.widgets import JSONCodeEdit

from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox, QScrollBar, QStyle, QStyleFactory, QToolBar, QTreeView, QTreeWidget, QTreeWidgetItem

import json 

def countLines(text):
    return len(text.split('\n'))

class JsonEditor(QtWidgets.QDockWidget):
    def __init__(self):
        super(JsonEditor, self).__init__()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Setting", "Value"])
        self.setWidget(self.tree)
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        self.setWindowTitle("Node Settings")
        self.callback = None
        self.root = QTreeWidgetItem(self.tree, ["Root"])
        self.tree.addTopLevelItem(self.root)
        


    def build_tree(self, dict, item : QTreeWidgetItem):
        for key, value in dict.items():
            if isinstance(value, Dict):
                child = QTreeWidgetItem([key])
                item.addChild(child)
                self.build_tree(value, child)
            elif isinstance(value, list):
                for entry in value:
                    strValue = str(entry)
                    child = QTreeWidgetItem(item, [key, strValue])
                    child.setFlags(child.flags() | Qt.ItemIsEditable)
                    item.addChild(child)
            else:
                strValue = str(value)
                child = QTreeWidgetItem(item, [key, strValue])
                child.setFlags(child.flags() | Qt.ItemIsEditable)
                item.addChild(child)
        



    def update(self, json_dict, callback, active):
       self.build_tree(json_dict, self.root)

    def apply_change(self):
        pass