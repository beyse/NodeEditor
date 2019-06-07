from nodeeditor.node_graphics_edge import QDMGraphicsEdge

from nodeeditor.utils import dumpException

DEBUG = False


class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.clear()
        self.history_limit = 32

        self._history_modified_listeners = []

    def clear(self):
        self.history_stack = []
        self.history_current_step = -1

    def storeInitialHistoryStamp(self):
        self.storeHistory("Initial History Stamp")

    def canUndo(self):
        return self.history_current_step > 0

    def canRedo(self):
        return self.history_current_step + 1 < len(self.history_stack)

    def undo(self):
        if DEBUG: print("UNDO")

        if self.canUndo():
            self.history_current_step -= 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def redo(self):
        if DEBUG: print("REDO")
        if self.canRedo():
            self.history_current_step += 1
            self.restoreHistory()
            self.scene.has_been_modified = True

    def addHistoryModifiedListener(self, callback):
        self._history_modified_listeners.append(callback)


    def restoreHistory(self):
        if DEBUG: print("Restoring history",
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])
        for callback in self._history_modified_listeners: callback()


    def storeHistory(self, desc, setModified=False):
        if setModified:
            self.scene.has_been_modified = True

        if DEBUG: print("Storing history", '"%s"' % desc,
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))

        # if the pointer (history_current_step) is not at the end of history_stack
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        hs = self.createHistoryStamp(desc)

        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print("  -- setting step to:", self.history_current_step)

        # always trigger history modified (for i.e. updateEditMenu)
        for callback in self._history_modified_listeners: callback()


    def createHistoryStamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges': [],
        }
        for item in self.scene.grScene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif isinstance(item, QDMGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj,
        }

        return history_stamp

    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp['desc'])

        try:
            self.scene.deserialize(history_stamp['snapshot'])

            # restore selection
            for edge_id in history_stamp['selection']['edges']:
                for edge in self.scene.edges:
                    if edge.id == edge_id:
                        edge.grEdge.setSelected(True)
                        break

            for node_id in history_stamp['selection']['nodes']:
                for node in self.scene.nodes:
                    if node.id == node_id:
                        node.grNode.setSelected(True)
                        break

        except Exception as e: dumpException(e)