from nodeeditor.node_socket import SocketDefinition
from PyQt5.QtWidgets import QLabel
from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt
from conf import register_node, OP_NODE_INPUT
from execution_node_base import ExecutionNode, GraphicsExecutionNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException


class CalcInputContent(QDMNodeContentWidget):
    def initUI(self):
        pass
    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


class CalcContent(QDMNodeContentWidget):
    def initUI(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

@register_node(OP_NODE_INPUT)
class CalcNode_Input(ExecutionNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INPUT
    op_title = "Adder"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs = [SocketDefinition("int", "in1"), SocketDefinition("foo", "in2"),], outputs=[SocketDefinition("int", "sum"), SocketDefinition("foo", "foo")])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcContent(self)
        self.grNode = GraphicsExecutionNode(self)

#    def evalImplementation(self):
#        
#        
#        #self.value = s_value
#        self.markDirty(False)
#        self.markInvalid(False)
#
#        self.markDescendantsInvalid(False)
#        self.markDescendantsDirty()
#
#        self.grNode.setToolTip("The input does not match")
#
#        self.evalChildren()
#
#        return False