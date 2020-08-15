DEBUG_REROUTING = True



class EdgeRerouting:
    def __init__(self, grView: 'QGraphicsView'):
        self.grView = grView
        self.start_socket = None        # store where we started re-routing the edges

    def print(self, *args):
        if DEBUG_REROUTING: print("REROUTING:", *args)

    def startRerouting(self, socket: 'Socket'):
        self.print("startRerouting", socket)
        self.start_socket = socket

    def stopRerouting(self, target: 'Socket'=None):
        self.print("stopRerouting on:", target, "no change" if target==self.start_socket else "")