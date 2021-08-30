from enum import Enum

import config
from packet import Packet
from edge import Edge

class State(Enum):
    BLACKOUT = 0
    ACTIVE = 1
    SLEEP = 2

class Node:
    def __init__(self, id, x, y):
        self.memory = 0
        self.energy = config.MAX_ENERGY
        self.state = State.ACTIVE
        self.delayTime = 0
        self.dropTask = 0
        self.totalConsumeEnergy = 0
        # self.blackoutCount = 0
        self.dropBlackoutTask = 0
        self.beforedropBlackout = 0
        Task = 0

        self.realTime = 0

        self.time = config.K
        self.skip = False

        self.id = id
        self.x = x
        self.y = y

    def sensing(self):
        self.memory = self.memory + (config.SENSING * config.K)

    def calc_local_processing_time(self) -> float:
        time = (1/config.NODE_CYCLE)*self.memory
        return time

    def calc_edge_processing_time(self, edge, packet) -> float:
        networkTime = (1/edge.speed)*packet.data
        packet.time = networkTime

        edgeTime = (1/config.EDGE_CYCLE)*packet.data
        return networkTime + edgeTime

    def consume_send_packet_energy(self, packet):
        # print("send energy" ,packet.data*config.TRANS_ENERGY)

        self.energy = self.energy - (packet.data*config.TRANS_ENERGY)       
        self.totalConsumeEnergy += packet.data*config.TRANS_ENERGY
        self.check_blackout()
        
    
    def consume_local_processing_energy(self):
        # print("local energy" ,self.memory * pow(config.NODE_CYCLE,2) * config.COEFF)

        self.energy = self.energy - (self.memory * pow(config.NODE_CYCLE,2) * config.COEFF)
        self.totalConsumeEnergy += (self.memory * pow(config.NODE_CYCLE,2) * config.COEFF)
        self.memory = 0
        self.check_blackout()

    def calc_consume_local_processing_energy(self):
        return (self.memory * pow(config.NODE_CYCLE,2) * config.COEFF)

    def calc_consume_send_packet_energy(self, packet):
        return (packet.data*config.TRANS_ENERGY)   

    def check_blackout(self):
        if self.energy <= config.BLACKOUT :
            self.state = State.BLACKOUT


            if self.energy < 0 :
                self.energy = 0

    def calc_harvest_energy(self, energy):
        # print(energy * config.PANEL)
        return (energy * config.PANEL)

    def harvest_energy(self, energy):
        self.energy +=energy
        if self.energy > config.BLACKOUT:
            self.state = State.ACTIVE

            if self.energy > config.MAX_ENERGY:
                self.energy = config.MAX_ENERGY
           


    