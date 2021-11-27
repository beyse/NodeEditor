import os

from pyqode.qt import QtWidgets
from pyqode.core import api, modes
from pyqode.json.widgets import JSONCodeEdit

from PyQt5.QtWidgets import QAction, QMessageBox, QStyle, QStyleFactory, QToolBar

import json 


class JsonEditor(QtWidgets.QMainWindow):
    def __init__(self, node_name, json_dict, callback):
        super(JsonEditor, self).__init__()
        self.editor = JSONCodeEdit(self)
        self.editor.setMinimumWidth(400)
        self.editor.setMinimumHeight(200)
        self.setCentralWidget(self.editor)
        self.callback = callback
        self.setWindowTitle('{} settings'.format(node_name))
        json_string = json.dumps(json_dict, indent = 2)
        self.original_content = json_string
        self.editor.setPlainText(json_string)

        toolbar = QToolBar("Editor Toolbar")

        self.done_action = QtWidgets.QAction("Done", self)
        self.done_action.setShortcut('Ctrl+S')
        self.done_action.triggered.connect(self.done)
        toolbar.addAction(self.done_action)
        
        self.undo_action = QtWidgets.QAction("Undo", self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.triggered.connect(self.editor.undo)
        toolbar.addAction(self.undo_action)

        self.redo_action = QtWidgets.QAction("Redo", self)
        self.redo_action.setShortcut('Ctrl+Y')
        self.redo_action.triggered.connect(self.editor.redo)
        toolbar.addAction(self.redo_action)

        self.restore_action = QtWidgets.QAction("Restore", self)
        self.restore_action.setShortcut('Ctrl+R')
        self.restore_action.triggered.connect(self.restore)
        toolbar.addAction(self.restore_action)

        self.addToolBar(toolbar)

    def restore(self):
        self.editor.setPlainText(self.original_content)

    def done(self):
        print('DONE')
        had_error = True
        json_dict = {}
        try:
            json_dict = json.loads(self.editor.toPlainText())
            had_error = False
        except:
            had_error = True
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("This JSON document is invalid.\nKeep open and continue editing?")
            msgBox.setWindowTitle("Syntax Error")
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Close)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Yes:
                return
            if returnValue == QMessageBox.Close:
                self.close()

        if had_error == False:
            self.callback(json_dict)
        
        self.close()