
from PyQt5.QtWidgets import QLabel
from nodeeditor.utils import dumpException
from nodeeditor.node_socket import SocketDefinition
from apps.execution_node_editor.execution_node_base import ExecutionNode, GraphicsExecutionNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
import re

LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_INPUT = 1
OP_NODE_OUTPUT = 2
OP_NODE_ADD = 3
OP_NODE_SUB = 4
OP_NODE_MUL = 5
OP_NODE_DIV = 6


CALC_NODES = {
}

node_counter = {

}

#class NodeTypeDefinition:
#    def __init__(self, type_name, input_sockets, output_sockets):
#        self.type_name = type_name
#        self.input_sockets = input_sockets
#        self.output_sockets = output_sockets


input_sockets = {
    #"ImageSourceNode": [SocketDefinition("int", "imageSourceIn"), SocketDefinition("int", "image source in 2")],
    #"CameraNode": [SocketDefinition("foo", "cameraNode 1")], 
    #"VideNode": [SocketDefinition("foo", "da video")]
}

output_sockets = {
    #"ImageSourceNode": [SocketDefinition("int", "out"), SocketDefinition("int", "oo"), SocketDefinition("int", "oo")],
    #"CameraNode": [SocketDefinition("foo", "hmm 1"), SocketDefinition("a", "hmm 2")], 
    #"VideNode": [SocketDefinition("foo", "oi video")]
}

nodeTypes = {
   
   # "Input": ["ImageSourceNode", "CameraNode", "VideNode"],
    #"Processing": ["AdderNode", "BlurNode", "BinarizeNode"],
    #"Output": ["VideWriterNode"]
} 

class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_types(node_type_definitions, category = "uncategorized"):

    for d in node_type_definitions:
        print(d.node_type)
        if d.node_type not in input_sockets.keys():
            input_sockets[d.node_type] = []
        for i in d.input_ports:
            print(i.port_name)
            socket_definition = SocketDefinition(i.data_type, i.port_name)
            input_sockets[d.node_type].append(socket_definition)

        if d.node_type not in output_sockets.keys():
            output_sockets[d.node_type] = []
        for o in d.output_ports:
            print(o.port_name)
            socket_definition = SocketDefinition(o.data_type, o.port_name)
            output_sockets[d.node_type].append(socket_definition)
        
        if category not in nodeTypes.keys():
            nodeTypes[category] = []
        nodeTypes[category].append(d.node_type)

class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

class ConcreteExecutionNode(ExecutionNode):
    op_code = OP_NODE_INPUT
    content_label_objname = "calc_node_input"

    def __init__(self, scene, node_type):
        print('node_type = {}'.format(node_type))
        self.node_type = node_type
        super().__init__(scene, inputs = input_sockets[node_type], outputs=output_sockets[node_type])
        self.op_title = node_type

        node_count = 1
        if node_type not in node_counter.keys():
            node_counter[node_type] = node_count
        else:
            node_counter[node_type] += 1
            node_count = node_counter[node_type]

        #postfix = ''
        #if node_count > 1:
        postfix = '_' + str(node_count)

        self.title = camel_to_snake(node_type) + postfix
        self.eval()

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = GraphicsExecutionNode(self)
        max_sockets = max(len(input_sockets[self.node_type]), len(output_sockets[self.node_type]))
        self.grNode.initSizes(max_sockets)
        self.grNode.initAssets()


def create_node(scene, node_type):
    return ConcreteExecutionNode(scene, node_type)
