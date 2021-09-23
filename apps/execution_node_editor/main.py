import os, sys
from qtpy.QtWidgets import QApplication

sys.path.insert(0, os.path.join( os.path.dirname(__file__), "..", ".." ))

from window import ExecutionNodeEditorWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    app.setStyle('Fusion')

    wnd = ExecutionNodeEditorWindow()
    wnd.show()

    sys.exit(app.exec_())
