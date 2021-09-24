
from PyQt5.QtWidgets import QLabel
from nodeeditor.utils import dumpException
from nodeeditor.node_socket import SocketDefinition
from apps.execution_node_editor.execution_node_base import ExecutionNode, GraphicsExecutionNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
import node_base

LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6


CALC_NODES = {
}

class NodeTypeDefinition:
    def __init__(self, type_name, input_sockets, output_sockets):
        self.type_name = type_name
        self.input_sockets = input_sockets
        self.output_sockets = output_sockets


input_sockets = {
    "ImageSourceNode": [SocketDefinition("int", "imageSourceIn"), SocketDefinition("int", "image source in 2")],
    "CameraNode": [SocketDefinition("foo", "cameraNode 1")], 
    "VideNode": [SocketDefinition("foo", "da video")]
}

output_sockets = {
    "ImageSourceNode": [SocketDefinition("int", "out"), SocketDefinition("int", "oo"), SocketDefinition("int", "oo")],
    "CameraNode": [SocketDefinition("foo", "hmm 1"), SocketDefinition("a", "hmm 2")], 
    "VideNode": [SocketDefinition("foo", "oi video")]
}

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass





class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)
class ConcreteExecutionNode(ExecutionNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    content_label_objname = "calc_node_input"

    def __init__(self, scene, node_type):
        self.node_type = node_type
        super().__init__(scene, inputs = input_sockets[node_type], outputs=output_sockets[node_type])
        self.op_title = node_type
        self.title = node_type
        self.eval()

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = GraphicsExecutionNode(self)
        max_sockets = max(len(input_sockets[self.node_type]), len(output_sockets[self.node_type]))
        self.grNode.initSizes(max_sockets)
        self.grNode.initAssets()


def create_node(scene, node_type):
    return ConcreteExecutionNode(scene, node_type)
