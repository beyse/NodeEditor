import os, sys
from PyQt5 import QtCore, QtGui
from qtpy.QtWidgets import QApplication

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

    wnd = ExecutionNodeEditorWindow()
    wnd.setWindowIcon(app_icon)
    wnd.show()

    sys.exit(app.exec_())
