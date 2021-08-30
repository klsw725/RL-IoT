import config

class Packet:
    def __init__(self, data, nodeid, packetid, time):
        self.data = data
        self.node = nodeid
        self.id = packetid
        self.time = time