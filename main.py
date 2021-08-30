import random
import pandas as pd

import config
from nodes import Node
from nodes import State
from edge import Edge
from packet import Packet

episode = [0,0,0,0,0]

# if __name__ == "__main__":
for i in range(0, config.EPISODES):
    nodes = []
    edges = []

    for i in range(0, config.NODES):
        nodes.append(Node(i, 0, 0))

    for i in range(0, config.EDGES):
        edges.append(Edge())

    solar = pd.read_csv('./solar.txt', names=['data'])

    for i in range(0, int(config.TIME/config.K)):
        random.shuffle(nodes)
        # before_R = float("inf")  
        # x = random.random()
        # x = random.randint(0, 5)/5
        for node in nodes:
            if node.state == State.ACTIVE:
                if not node.skip:
                    # node.sensing()

                    
                    # before_x = x
                 
                    # x = random.randint(0, 5)/5
                    # x = 1
                    y = random.randint(0, config.EDGES - 1)

                    packet = Packet(400000, node.id, i, 0)
                    # node.memory = node.memory - packet.data
                    

                    # localTime = node.calc_local_processing_time()
                    edgeTime = node.calc_edge_processing_time(edges[y], packet)

                    # localEnergy = node.calc_consume_local_processing_energy()
                    edgeEnergy = node.calc_consume_send_packet_energy(packet)

                    localTime=0

                    # R = localTime + edgeTime + localEnergy + edgeEnergy

                    # if R > before_R :
                    #     node.memory = config.SENSING
                    #     packet = Packet(before_x*node.memory, node.id, i, 0)
                    #     node.memory = node.memory - packet.data


                    #     localTime = node.calc_local_processing_time()
                    #     edgeTime = node.calc_edge_processing_time(edges[y], packet)
                    # else:
                    #     before_R = R

                    node.realTime += (edgeTime)

                    edges[y].calc_network(packet)

                    # node.consume_local_processing_energy()
                    node.consume_send_packet_energy(packet)

                    # print("localTime: ", localTime, " edgeTime: ", edgeTime)
                    # a = input('').split(" ")[0]

                    # print(node.energy)
                    if edgeTime <= node.time:
                        node.time = config.K

                    # elif localTime > node.time:
                    #     delayTime = localTime - node.time
                    #     if delayTime >= config.K:
                    #         node.dropTask += 1
                    #         node.delayTime += config.K
                    #         node.skip = True
                    #         node.time = delayTime
                    #     else:
                    #         node.delayTime += delayTime
                    #         node.time = config.K - delayTime

                    elif edgeTime > node.time:
                        # print("edgeTime")
                        delayTime = edgeTime - node.time
                        if delayTime > config.K:
                            if localTime < edgeTime:
                                node.delayTime += config.K

                        else:
                            if localTime < edgeTime:
                                node.delayTime += (edgeTime - localTime)

                else:
                    delayTime= node.time - config.K
                    
                    if delayTime >= config.K:
                        node.dropTask += 1
                        node.delayTime += config.K
                        node.time = delayTime
                        node.skip = True

                    else:
                        node.skip = False
                        node.delayTime += delayTime
                        node.time = config.K - delayTime
                    #    node.delayTime += delayTime
            else:
                # node.blackoutCount += 1
                node.dropBlackoutTask += 1
                # node.delayTime += config.K

            harvestEnergy = node.calc_harvest_energy(
                solar['data'][i % len(solar['data'])])
            node.harvest_energy(harvestEnergy)

        # print(nodes[0].energy)
        # print(nodes[0].delayTime)
        # print(nodes[0].dropTask)
        # print("\n")
        # a = input('').split(" ")[0]

        for edge in edges:
            edge.flush()

    for node in nodes:
        print(node.dropBlackoutTask)
        print(node.realTime)
        print(node.dropTask)
        # print(node.blackoutCount)
        print("\n")

        episode[0] += node.dropBlackoutTask
        episode[1] += node.realTime
        episode[2] += node.dropTask
        # episode[3] += node.blackoutCount


print("-------------------------------------------")
for i in range(0,len(episode)):
    episode[i] /= (config.NODES * config.EPISODES)
    print(episode[i])