# -*- coding: utf-8 -*-
"""
A module containing Graphics representation of :class:`~nodeeditor.node_node.Node`
"""
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QFontMetrics, QTextBlockFormat, QTextCursor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from qtpy.QtWidgets import QGraphicsItem, QWidget, QGraphicsTextItem
from qtpy.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
from qtpy.QtCore import Qt, QRectF


class QDMGraphicsNode(QGraphicsItem):
    """Class describing Graphics representation of :class:`~nodeeditor.node_node.Node`"""

    def __init__(self, node: 'Node', parent: QWidget = None):
        """
        :param node: reference to :class:`~nodeeditor.node_node.Node`
        :type node: :class:`~nodeeditor.node_node.Node`
        :param parent: parent widget
        :type parent: QWidget

        :Instance Attributes:

            - **node** - reference to :class:`~nodeeditor.node_node.Node`
        """
        super().__init__(parent)
        self.node = node

        # init our flags
        self.hovered = False
        self._was_moved = False
        self._last_selected_state = False
        self.initSizes(0)
        self.initAssets()
        self.initUI()



    @property
    def content(self):
        """Reference to `Node Content`"""
        return self.node.content if self.node else None

    @property
    def title(self):
        """title of this `Node`

        :getter: current Graphics Node title
        :setter: stores and make visible the new title
        :type: str
        """
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def initUI(self):
        """Set up this ``QGraphicsItem``"""
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # init title
        self.initTitle()
        self.title = self.node.title

        self.initContent()

    def initSizes(self):
        """Set up internal attributes like `width`, `height`, etc."""
        self.width = 180
        self.height = 240
        self.edge_roundness = 1.0
        self.edge_padding = 10.0
        self.title_height = 24.0
        self.title_horizontal_padding = 4.0
        self.title_vertical_padding = 4.0

    def initAssets(self):
        """Initialize ``QObjects`` like ``QColor``, ``QPen`` and ``QBrush``"""
        self._title_color = QColor("#ffffff")
        self._title_font = QFont("Roboto", 10)

        self._color_hovered = QColor("#52ffb9")
        self._color_selected = QColor("#28daed")
        self._color_dirty = QColor("#ed8836")
        self._color_dirty_selected = QColor("#ffc519")

        self._pen_default = QPen(QColor("#00000000"))
        self._pen_default.setWidthF(0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(1.5)
        self._pen_dirty = QPen(self._color_dirty)
        self._pen_dirty.setWidthF(1.5)
        self._pen_dirty_selected = QPen(self._color_dirty_selected)
        self._pen_dirty_selected.setWidthF(1.5)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(2)

        self._brush_title = QBrush(QColor("#1b202c"))
        self._brush_title_hover = QBrush(QColor("#222736"))
        self._brush_title_selected = QBrush(QColor("#282f40"))
        self._brush_title_dirty = QBrush(self._color_dirty)
        self._brush_title_dirty_selected = QBrush(self._color_dirty_selected)
        self._brush_title_dirty_hovered = QBrush(QColor("#f29d33"))
        self._brush_background = QBrush(QColor("#151a24"))
        self._brush_hover = QBrush(QColor("#151a24"))

        shadowX = 0
        shadowY = 0
        self.__shadow = QGraphicsDropShadowEffect(blurRadius=0,
                                                  offset=QPoint(shadowX, shadowY))
        self._color_shadow = QColor('#000000')
        self.__shadow.setColor(self._color_shadow)
        self.__shadow.setEnabled(True)
        self.setGraphicsEffect(self.__shadow)

        self.width += shadowX
        self.height += shadowY

    def onSelected(self):
        """Our event handling when the node was selected"""
        self.node.scene.grScene.itemSelected.emit()

    def doSelect(self, new_state=True):
        """Safe version of selecting the `Graphics Node`. Takes care about the selection state flag used internally

        :param new_state: ``True`` to select, ``False`` to deselect
        :type new_state: ``bool``
        """
        self.setSelected(new_state)
        self._last_selected_state = new_state
        if new_state:
            self.onSelected()

    def mouseMoveEvent(self, event):
        """Overridden event to detect that we moved with this `Node`"""
        super().mouseMoveEvent(event)

        # optimize me! just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self._was_moved = True

    def mouseReleaseEvent(self, event):
        """Overriden event to handle when we moved, selected or deselected this `Node`"""
        super().mouseReleaseEvent(event)

        # handle when grNode moved
        if self._was_moved:
            self._was_moved = False
            self.node.scene.history.storeHistory(
                "Node moved", setModified=True)

            self.node.scene.resetLastSelectedStates()
            self.doSelect()     # also trigger itemSelected when node was moved

            # we need to store the last selected state, because moving does also select the nodes
            self.node.scene._last_selected_items = self.node.scene.getSelectedItems()

            # now we want to skip storing selection
            return

        # handle when grNode was clicked on
        if self._last_selected_state != self.isSelected() or self.node.scene._last_selected_items != self.node.scene.getSelectedItems():
            self.node.scene.resetLastSelectedStates()
            self._last_selected_state = self.isSelected()
            self.onSelected()

    def mouseDoubleClickEvent(self, event):
        """Overriden event for doubleclick. Resend to `Node::onDoubleClicked`"""
        self.node.onDoubleClicked(event)

    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """Handle hover effect"""
        self.hovered = False
        self.update()

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initTitle(self):
        """Set up the title Graphics representation: font, color, position, etc."""
        self.title_item = QGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        metrics = QFontMetrics(self._title_font)
        width = metrics.width(self.node.title)
        self.title_item.setFont(self._title_font)
        self.title_item.setX(1)
        self.title_item.setY(0)
        self.title_item.setTextWidth(self.width)

    def initContent(self):
        pass
        # """Set up the `grContent` - ``QGraphicsProxyWidget`` to have a container for `Graphics Content`"""
        # if self.content is not None:
        #     print(type(self.content))
        #     self.content.setGeometry(self.edge_padding, self.title_height + self.edge_padding,
        #                          self.width - 2 * self.edge_padding, self.height - 2 * self.edge_padding - self.title_height)

        # # get the QGraphicsProxyWidget when inserted into the grScene
        # self.grContent = self.node.scene.grScene.addWidget(self.content)
        # self.grContent.node = self.node
        # self.grContent.setParentItem(self)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """Painting the rounded rectanglar `Node`"""
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(
            0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness,
                           self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height -
                           self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        if self.hovered:
            if self.node.isDirty():
                painter.setBrush(self._brush_title_dirty_hovered)
            else:
                painter.setBrush(self._brush_title_hover)
        else:
            if self.node.isDirty():
                painter.setBrush(self._brush_title_dirty)
            else:
                painter.setBrush(self._brush_title)

        if self.isSelected():
            self.__shadow.setBlurRadius(20)
            if self.node.isDirty():
                painter.setBrush(self._brush_title_dirty_selected)
                self.__shadow.setColor(self._color_dirty)
            else:
                painter.setBrush(self._brush_title_selected)
                self.__shadow.setColor(self._color_selected)

        else:
            self.__shadow.setColor(QColor('#00000000'))
            self.__shadow.setBlurRadius(0)


        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height -
                                    self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height,
                             self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness,
                             self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)

        if self.hovered:
            painter.setBrush(self._brush_hover)
            painter.drawPath(path_content.simplified())

        else:
            painter.setBrush(self._brush_background)
            painter.drawPath(path_content.simplified())

            # outline
        path_outline = QPainterPath()
        painter.setBrush(Qt.NoBrush)
        if self.isSelected():
            painter.setPen(self._pen_selected)
            path_outline.addRoundedRect(
                0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        else:
            painter.setPen(self._pen_default)
            path_outline.addRoundedRect(-0.5, -0.5, self.width+1,
                                        self.height+1, self.edge_roundness, self.edge_roundness)

        if self.node.isDirty():
            if self.isSelected():
                painter.setPen(self._pen_dirty_selected)
            else:
                painter.setPen(self._pen_dirty)

        painter.drawPath(path_outline.simplified())
