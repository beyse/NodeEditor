from PyQt5.QtWidgets import *
from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode


class CalcGraphicsNode(QDMGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 74
        self.edge_size = 5
        self._padding = 8


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class CalcNode(Node):
    def __init__(self, scene, op_code, op_title, content_label="", content_label_objname="calc_node_bg", inputs=[2,2], outputs=[1]):
        self.op_code = op_code
        self.op_title = op_title
        self.content_label = content_label
        self.content_label_objname = content_label_objname

        super().__init__(scene, self.op_title, inputs, outputs)

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = CalcGraphicsNode(self)