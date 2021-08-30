import config
from packet import Packet

class Edge:
    def __init__(self):
        self.network: List[packet] = []
        self.dataCount = 0
        self.speed = config.NETWORK_V
        self.bandwidth = config.BANDWIDTH

    def flush(self):
        self.dataCount = 0
        self.bandwidth = config.BANDWIDTH

        for packet in self.network:
            if packet.time < config.K:
                del packet
            else:
                self.dataCount += 1
                self.bandwidth -= packet.data

        self.speed = config.NETWORK_V/(1+self.dataCount)

    def calc_network(self, packet):
        self.network.append(packet)
        self.bandwidth -= packet.data

        if self.bandwidth < 0:
            self.bandwidth = 0
            self.speed = config.NETWORK_V / (len(self.network) + 1)


