from json.decoder import JSONDecodeError
import os
from subprocess import call
from PyQt5 import QtCore
from PyQt5.QtGui import QBrush, QColor, QCursor
from pyqode.core.api import syntax_highlighter
from pyqode.core.api.decoration import TextDecoration
import re

from pyqode.qt import QtWidgets
from pyqode.json.widgets import JSONCodeEdit

from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox, QScrollBar, QStyle, QStyleFactory, QToolBar

import json 

def countLines(text):
    return len(text.split('\n'))

class JsonEditor(QtWidgets.QDockWidget):
    def __init__(self):
        super(JsonEditor, self).__init__()
        self.editor = JSONCodeEdit(parent=self, interpreter=None)
        self.editor.setHorizontalScrollBar(QScrollBar(self.editor))
        self.editor.tab_length = 2
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        self.editor.setMinimumWidth(100)
        self.editor.setMinimumHeight(100)
        self.editor.textChanged.connect(self.apply_change)
        self.setWidget(self.editor)
        self.setWindowTitle("Node Settings")
        self.callback = None

    def update(self, json_dict, callback, active):
        self.editor.decorations.clear()
        if not active:
            self.setWidget(None)
        else:
            self.setWidget(self.editor)
        self.editor.setEnabled(active)            
        self.callback = callback
        json_string = json.dumps(json_dict, indent = 2)
        self.original_content = json_string
        self.editor.setPlainText(json_string)

    def restore(self):
        self.editor.setPlainText(self.original_content)

    def apply_change(self):
        self.editor.decorations.clear()
        self.setToolTip('')
        self.setToolTipDuration(0)
        had_error = True
        json_dict = {}
        try:
            json_dict = json.loads(self.editor.toPlainText())
            had_error = False
        except JSONDecodeError as ex:
            numbers = re.findall(r'\d+', str(ex))
            line = int(numbers[0])
            line -= 1
            column = int(numbers[1])
            char = int(numbers[2])
            decoration = TextDecoration(self.editor.document(), char, char, line, line, 99, str(ex), True)
            decoration.cursor.setPosition(char)            
            decoration.set_as_error()
            self.editor.decorations.append(decoration)
            self.setToolTip(str(ex))
            self.setToolTipDuration(25000)
            had_error = True

        if had_error == False and self.callback is not None:
            print('Apply new settings to node')
            self.callback(json_dict)