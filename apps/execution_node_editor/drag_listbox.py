from PyQt5.QtGui import QBrush, QColor, QFont
from apps.execution_node_editor.conf import LISTBOX_MIMETYPE, nodeTypes
from qtpy.QtGui import QPixmap, QIcon, QDrag
from qtpy.QtCore import QSize, Qt, QByteArray, QDataStream, QMimeData, QIODevice, QPoint
from qtpy.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem 

from nodeeditor.utils import dumpException

class QDMDragListbox(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # init
        self.setIconSize(QSize(32, 32))
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setColumnCount(1)
        self.setHeaderLabels([""])
        self.addMyItems()
        self._font = QFont("Arial", 12)
        self.setFont(self._font)
        


    def addMyItems(self):
        items = []
        for key, values in nodeTypes.items():
            item = QTreeWidgetItem([key])
            color = QColor("#ffffff")
            brush = QBrush(color)
            item.setForeground(0, brush)
            for value in values:
                child = QTreeWidgetItem([value])
                child.setForeground(0, brush)
                child.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)
                # setup data
                child.setData(0, Qt.UserRole + 1, 0)
                item.addChild(child)
            items.append(item)
        
        self.insertTopLevelItems(0, items)
        #keys = list(CALC_NODES.keys())
        #keys.sort()
        #for key in keys:
        #    node = get_class_from_opcode(key)
        #    self.addMyItem(node.op_title, node.icon, node.op_code)

    def startDrag(self, *args, **kwargs):
        try:
            print("startDrag")
            item = self.currentItem()
            op_code = item.data(0, Qt.UserRole + 1)

            pixmap = QPixmap(".")


            itemData = QByteArray()
            dataStream = QDataStream(itemData, QIODevice.WriteOnly)
            dataStream << pixmap
            dataStream.writeInt(op_code)
            dataStream.writeQString(item.text(0))

            mimeData = QMimeData()
            mimeData.setData(LISTBOX_MIMETYPE, itemData)

            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setHotSpot(QPoint(pixmap.width() / 2, pixmap.height() / 2))
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)

        except Exception as e: dumpException(e)