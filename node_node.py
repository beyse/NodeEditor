from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        self.inputs = []
        self.outputs = []

