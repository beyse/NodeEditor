import math
from qtpy.QtCore import QPointF
from qtpy.QtGui import QPainterPath


class GraphicsEdgePathBase:
    """Base Class for calculating the graphics path to draw for an graphics Edge"""

    def __init__(self, owner: 'QDMGraphicsEdge'):
        # keep the reference to owner GraphicsEdge class
        self.owner = owner

    def calcPath(self):
        """Calculate the Direct line connection

        :returns: ``QPainterPath`` of the graphics path to draw
        :rtype: ``QPainterPath`` or ``None``
        """
        return None


class GraphicsEdgePathDirect(GraphicsEdgePathBase):
    """Direct line connection Graphics Edge"""
    def calcPath(self) -> QPainterPath:
        """Calculate the Direct line connection

        :returns: ``QPainterPath`` of the direct line
        :rtype: ``QPainterPath``
        """
        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.lineTo(self.owner.posDestination[0], self.owner.posDestination[1])
        return path


class GraphicsEdgePathBezier(GraphicsEdgePathBase):
    """Cubic line connection Graphics Edge"""
    def calcPath(self) -> QPainterPath:
        """Calculate the cubic Bezier line connection with 2 control points

        :returns: ``QPainterPath`` of the cubic Bezier line
        :rtype: ``QPainterPath``
        """
        s = self.owner.posSource
        d = self.owner.posDestination
        distX = abs(d[0] - s[0])
        c1x = +distX * 0.55
        c2x = -distX * 0.25
        c1y = 0
        c2y = 0

        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.cubicTo( 
            s[0] + c1x, s[1] + c1y, 
            d[0] + c2x, d[1] + c2y, 
            self.owner.posDestination[0], 
            self.owner.posDestination[1])
        return path


class GraphicsEdgePathSquare(GraphicsEdgePathBase):
    """Square line connection Graphics Edge"""
    def __init__(self, *args, handle_weight=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self.rand = None
        self.handle_weight = handle_weight

    def calcPath(self):
        """Calculate the square edge line connection

        :returns: ``QPainterPath`` of the edge square line
        :rtype: ``QPainterPath``
        """

        s = self.owner.posSource
        d = self.owner.posDestination

        mid_x = s[0] + ((d[0] - s[0]) * self.handle_weight)

        path = QPainterPath(QPointF(s[0], s[1]))
        path.lineTo(mid_x, s[1])
        path.lineTo(mid_x, d[1])
        path.lineTo(d[0], d[1])

        return path
