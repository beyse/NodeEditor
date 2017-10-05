from node_graphics_edge import *


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = True

class Edge:
    def __init__(self, scene, start_socket, end_socket, type=EDGE_TYPE_DIRECT):

        self.scene = scene

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.grEdge = QDMGraphicsEdgeDirect(self) if type==EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()
        if DEBUG: print("Edge: ", self.grEdge.posSource, "to", self.grEdge.posDestination)
        self.scene.grScene.addItem(self.grEdge)

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        if DEBUG: print(" SS:", self.start_socket)
        if DEBUG: print(" ES:", self.end_socket)
        self.grEdge.update()


    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None


    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)