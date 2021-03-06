# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of a :class:`~nodeeditor.node_socket.Socket`
"""
from PyQt5.QtGui import QFont, QFontMetrics, QPainterPath
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from qtpy.QtWidgets import QGraphicsItem
from qtpy.QtGui import QColor, QBrush, QPen
from qtpy.QtCore import Qt, QRectF


class QDMGraphicsSocket(QGraphicsItem):
    """Class representing Graphic `Socket` in ``QGraphicsScene``"""
    def __init__(self, socket:'Socket'):
        """
        :param socket: reference to :class:`~nodeeditor.node_socket.Socket`
        :type socket: :class:`~nodeeditor.node_socket.Socket`
        """
        super().__init__(socket.node.grNode)

        self.socket = socket

        self.isHighlighted = False

        self.radius = 6.0
        self.outline_width = 0.5
        self.initAssets()

    @property
    def socket_type(self):
        return self.socket.socket_type

    @property
    def socket_name(self):
        return self.socket.socket_name

    def getSocketColor(self, key):
        return QColor("#1294ba")

    def changeSocketType(self):
        """Change the Socket Type"""
        self._color_background = self.getSocketColor(self.socket_type)
        self._brush = QBrush(self._color_background)
        # print("Socket changed to:", self._color_background.getRgbF())
        self.update()

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""

        self.setToolTip(self.socket_type)

        # determine socket color
        self._color_background = self.getSocketColor(self.socket_type)
        self._color_outline = QColor("#FFFFFF")
        self._color_highlight = QColor("#28daed")
        self._color_invalid = QColor("#ed8836")

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._pen_highlight = QPen(QColor('#FFFFFF'))
        self._pen_highlight.setWidthF(1.0)
        self._brush = QBrush(self._color_background)
        self._brush_highlight = QBrush(self._color_highlight)
        self._brush_invalid = QBrush(self._color_invalid)

        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self._title_color = QColor("#a2abba")
        self._title_color_highlighted = QColor("#28daed")
        self._title_font = QFont("Roboto", 10)
        self.title_horizontal_padding = 8.0
        self.title_vertical_padding = 6.0
        self.width = 100
        self.title_height = 20,
        self.edge_roundness = 0
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)

        
        self.title_item.setTextWidth(
            self.width
            - 2 * self.title_horizontal_padding
        )
        # title

        if self.socket.is_input:
            text = str(self.socket_name)
            metrics = QFontMetrics(self._title_font)
            width = metrics.width(text)
            height = metrics.height()
            self.title_item.setPlainText(text)
            self.title_item.setPos(5, -12)
        elif self.socket.is_output:
            text = str(self.socket_name)
            metrics = QFontMetrics(self._title_font)
            width = metrics.width(text)
            height = metrics.height()
            self.title_item.setPlainText(text)
            self.title_item.setPos(-(width+12), -12)

        self.path_title = QPainterPath()
        self.path_title.setFillRule(Qt.WindingFill)
        self._brush_title = QBrush(QColor("#000000"))


    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting a circle"""

        if self.socket.is_valid:
            painter.setBrush(self._brush if not self.isHighlighted else self._brush_highlight)
            painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
            painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
            painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(self._brush_invalid)
            painter.setPen(self._pen if not self.isHighlighted else self._pen_highlight)
            painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
            painter.setPen(Qt.NoPen)

        if self.isHighlighted:
            self.title_item.setDefaultTextColor(self._title_color_highlighted)
        else:
            self.title_item.setDefaultTextColor(self._title_color)



    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )