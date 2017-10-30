DEBUG = True


class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 8

    def undo(self):
        if DEBUG: print("UNDO")

        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        if DEBUG: print("REDO")
        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()


    def restoreHistory(self):
        if DEBUG: print("Restoring history",
                        ".... current_step: @%d" % self.history_current_step,
                        "(%d)" % len(self.history_stack))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])


    def storeHistory(self, desc):
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


    def createHistoryStamp(self, desc):
        return desc

    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print("RHS: ", history_stamp)