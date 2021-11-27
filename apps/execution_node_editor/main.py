import os, sys
from PyQt5 import QtCore, QtGui
from qtpy.QtWidgets import QApplication
import ctypes
from sys import platform


sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from window import ExecutionNodeEditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    app_icon = QtGui.QIcon()
    app_icon.addFile('gui/icons/16x16.png', QtCore.QSize(16,16))
    app_icon.addFile('gui/icons/24x24.png', QtCore.QSize(24,24))
    app_icon.addFile('gui/icons/32x32.png', QtCore.QSize(32,32))
    app_icon.addFile('gui/icons/48x48.png', QtCore.QSize(48,48))
    app_icon.addFile('gui/icons/64x64.png', QtCore.QSize(64,64))
    app_icon.addFile('gui/icons/128x128.png', QtCore.QSize(128,128))
    app_icon.addFile('gui/icons/256x256.png', QtCore.QSize(256,256))
    app.setWindowIcon(app_icon)


    if platform == "win32":
        # Windows...
        #This will make sure that the app icon is set in the taskbar on windows
        # See https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105 
        myappid = u'no-company.node-editor.execution-graph-editor.1.0' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    wnd = ExecutionNodeEditorWindow()
    wnd.setWindowIcon(app_icon)
    wnd.show()
    wnd.actNew.trigger()

    sys.exit(app.exec_())
