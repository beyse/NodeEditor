from node_graphics_node import QDMGraphicsNode


class Node():
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.grNode = QDMGraphicsNode(self, self.title)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        self.inputs = []
        self.outputs = []

