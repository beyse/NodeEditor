from examples.example_calculator.calc_conf import *
from examples.example_calculator.calc_node_base import *


@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_ADD, "Add", "+")

@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_SUB, "Substract", "-")

@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_MUL, "Multiply", "*")

@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_DIV, "Divide", "/")

@register_node(OP_NODE_INPUT)
class CalcNode_Input(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_INPUT, "Input", inputs=[], outputs=[3])

@register_node(OP_NODE_OUTPUT)
class CalcNode_Output(CalcNode):
    def __init__(self, scene):
        super().__init__(scene, OP_NODE_OUTPUT, "Output", inputs=[1], outputs=[])


# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)