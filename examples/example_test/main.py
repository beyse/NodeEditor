import sys
from PyQt5.QtWidgets import *

from nodeeditor.node_editor_window import NodeEditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    wnd = NodeEditorWindow()

    sys.exit(app.exec_())
