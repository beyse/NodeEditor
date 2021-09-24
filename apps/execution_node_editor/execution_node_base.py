from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.node_node import Node
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.node_graphics_node import QDMGraphicsNode
from nodeeditor.node_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.utils import dumpException


class GraphicsExecutionNode(QDMGraphicsNode):


    def initSizes(self, max_sockets):
        super().initSizes()
        self.width = 150
        self.height = 35 + 22*max_sockets
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def initAssets(self):
        super().initAssets()

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        offset = 24.0
        if self.node.isDirty(): offset = 0.0
        if self.node.isInvalid(): offset = 48.0

class ExecutionContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)


class ExecutionNode(Node):
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "execution_node_bg"

    GraphicsNode_class = GraphicsExecutionNode
    NodeContent_class = ExecutionContent

    def __init__(self, scene, inputs=[2,2], outputs=[1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None
        # it's really important to mark all nodes Dirty by default
        self.markDirty()



    def initSettings(self):
        super().initSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def evalOperation(self, input1, input2):
        return 123

    def evalImplementation(self):
        input_sockets = self.getInputSockets()
        print("eval. There are {} input sockets".format(len(input_sockets)))
        self.markInvalid(False)
        self.markDirty(False)

        for input_socket in input_sockets:
            print("input socket name = {}".format(input_socket.socket_name))
            print("input socket type = {}".format(input_socket.socket_type))
            if len(input_socket.edges) == 0:
                print("This socket has no edges") 
                input_socket.is_valid = True
                continue
            else:
                print("This socket has {} edges".format(len(input_socket.edges))) 

            connecting_edge = input_socket.edges[0]
            print(connecting_edge)
            start_socket = connecting_edge.getStartSocket()
            if start_socket is None:
                print("start socket is none")
                input_socket.is_valid = True
            else:
                print("start socket name = {}".format(start_socket.socket_name))
                print("start socket type = {}".format(start_socket.socket_type))
            if start_socket.socket_type != input_socket.socket_type:
                self.markInvalid(True)
                self.markDirty(True)
                connecting_edge.is_valid = False
                input_socket.is_valid = False
            else:
                connecting_edge.is_valid = True
                input_socket.is_valid = True
        return True

    def eval(self):
        if not self.isDirty() and not self.isInvalid():
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:

            val = self.evalImplementation()
            return val
        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsDirty()
        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)



    def onInputChanged(self, socket=None):
        print("%s::__onInputChanged" % self.__class__.__name__)
        self.markDirty()
        self.eval()


    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res