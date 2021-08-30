import random
import pandas as pd
import numpy as np

import config
from nodes import Node
from nodes import State
from edge import Edge
from packet import Packet


#import libraries


# define the    shape of the environment (i.e., its states)
environment_rows = config.NODES
environment_columns = config.EDGES
environment_state = (round(config.NETWORK_V/1000000)+10,
                     100, round(config.MAX_ENERGY/1000)+10)
# Create a 3D numpy array to hold the current Q-values for each state and action pair: Q(s, a)
# The array contains 11 rows and 11 columns (to match the shape of the environment), as well as a third "action" dimension.
# The "action" dimension consists of 4 layers that will allow us to keep track of the Q-values for each possible action in
# each state (see next cell for a description of possible actions).
# The value of each (state, action) pair is initialized to 0.
q_values = np.zeros(environment_state + (6*config.EDGES,))
# q_values = []
# for i in range(0, config.NODES):
#     q_values.append(q_values1)
    
# define actions
# numeric action codes: 0 = up, 1 = right, 2 = down, 3 = left
actions = ['edge1 + 0/5', 'edge1 + 1/5', 'edge1 + 2/5', 'edge1 + 3/5', 'edge1 + 4/5', 'edge1 + 5/5',
           'edge2 + 0/5', 'edge2 + 1/5', 'edge2 + 2/5', 'edge2 + 3/5', 'edge2 + 4/5', 'edge2 + 5/5',
           'edge3 + 0/5', 'edge3 + 1/5', 'edge3 + 2/5', 'edge3 + 3/5', 'edge3 + 4/5', 'edge3 + 5/5', 'edge3 + 6/10', 'edge3 + 7/10', 'edge3 + 8/10', 'edge3 + 9/10', 'edge3 + 10/10']

# Create a 2D numpy array to hold the rewards for each state.
# The array contains 11 rows and 11 columns (to match the shape of the environment), and each value is initialized to -100.
# rewards = np.full((environment_rows, environment_columns), -100.)
# rewards[0,
#         5] = 100.  # set the reward for the packaging area (i.e., the goal) to 100
# define aisle locations (i.e., white squares) for rows 1 through 9
# aisles = {}  # store locations in a dictionary
# aisles[1] = [i for i in range(1, 10)]
# aisles[2] = [1, 7, 9]
# aisles[3] = [i for i in range(1, 8)]
# aisles[3].append(9)
# aisles[4] = [3, 7]
# aisles[5] = [i for i in range(11)]
# aisles[6] = [5]
# aisles[7] = [i for i in range(1, 10)]
# aisles[8] = [3, 7]
# aisles[9] = [i for i in range(11)]
# set the rewards for all aisle locations (i.e., white squares)
# for row_index in range(1, 10):
#     for column_index in aisles[row_index]:
#         rewards[row_index, column_index] = -1.
# print rewards matrix
# for row in rewards:
#     print(row)

# define a function that determines if the specified location is a terminal state


# def is_terminal_state(current_row_index, current_column_index):
#     # if the reward for this location is -1, then it is not a terminal state (i.e., it is a 'white square')
#     if rewards[current_row_index, current_column_index] == -1.:
#         return False
#     else:
#         return True
# # define a function that will choose a random, non-terminal starting location


# def get_starting_location():
#     # get a random row and column index
#     current_row_index = np.random.randint(environment_rows)
#     current_column_index = np.random.randint(environment_columns)
#     # continue choosing random row and column indexes until a non-terminal state is identified
#     # (i.e., until the chosen state is a 'white square').
#     while is_terminal_state(current_row_index, current_column_index):
#         current_row_index = np.random.randint(environment_rows)
#         current_column_index = np.random.randint(environment_columns)
#     return current_row_index, current_column_index
# # define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)

def get_init_state(i, nodes, edges):
    # get a random row and column index
    energy = 0
    for node in nodes:
        energy += node.energy
    energy = energy / len(nodes)

    speed = 0
    for edge in edges:
        speed += edge.speed
    speed = speed / len(edges)

    return tuple([round(speed/1000000), 0, round(energy/1000)])
    # return tuple([round(speed/1000000), round(solar['data'][i % len(solar['data']) + 21600]*1000), round(energy/1000)])


# def get_next_action(current_row_index, current_column_index, epsilon):
#     # if a randomly chosen value between 0 and 1 is less than epsilon,
#     # then choose the most promising value from the Q-table for this state.
#     if np.random.random() < epsilon:
#         return np.argmax(q_values[current_row_index, current_column_index])
#     else:  # choose a random action
#         return np.random.randint(len(actions))
# # define a function that will get the next location based on the chosen action

def get_next_action(id, state, epsilon):
    # if a randomly chosen value between 0 and 1 is less than epsilon,
    # then choose the most promising value from the Q-table for this state.
    if np.random.random() < epsilon:
        return np.random.randint(6*config.EDGES)
    else:  # choose a random action
        return np.argmax(q_values[state])
        
# define a function that will get the next location based on the chosen action


def get_next_location(action_index):
    newEdge = 0
    newRatio = 0
    if actions[action_index] == 'edge1 + 0/5':
        newEdge = 0
        newRatio = 0
    elif actions[action_index] == 'edge1 + 1/5':
        newEdge = 0
        newRatio = 1/5
    elif actions[action_index] == 'edge1 + 2/5':
        newEdge = 0
        newRatio = 2/5
    elif actions[action_index] == 'edge1 + 3/5':
        newEdge = 0
        newRatio = 3/5
    elif actions[action_index] == 'edge1 + 4/5':
        newEdge = 0
        newRatio = 4/5
    elif actions[action_index] == 'edge1 + 5/5':
        newEdge = 0
        newRatio = 1
    elif actions[action_index] == 'edge2 + 0/5':
        newEdge = 1
        newRatio = 0
    elif actions[action_index] == 'edge2 + 1/5':
        newEdge = 1
        newRatio = 1/5
    elif actions[action_index] == 'edge2 + 2/5':
        newEdge = 1
        newRatio = 2/5
    elif actions[action_index] == 'edge2 + 3/5':
        newEdge = 1
        newRatio = 3/5
    elif actions[action_index] == 'edge2 + 4/5':
        newEdge = 1
        newRatio = 4/5
    elif actions[action_index] == 'edge2 + 5/5':
        newEdge = 1
        newRatio = 1
    elif actions[action_index] == 'edge3 + 0/5':
        newEdge = 2
        newRatio = 0
    elif actions[action_index] == 'edge3 + 1/5':
        newEdge = 2
        newRatio = 1/5
    elif actions[action_index] == 'edge3 + 2/5':
        newEdge = 2
        newRatio = 2/5
    elif actions[action_index] == 'edge3 + 3/5':
        newEdge = 2
        newRatio = 3/5
    elif actions[action_index] == 'edge3 + 4/5':
        newEdge = 2
        newRatio = 4/5
    elif actions[action_index] == 'edge3 + 5/5':
        newEdge = 2
        newRatio = 1
    return newEdge, newRatio
# Define a function that will get the shortest path between any location within the warehouse that
# the robot is allowed to travel and the item packaging location.


# def get_shortest_path(start_row_index, start_column_index):
#     # return immediately if this is an invalid starting location
#     if is_terminal_state(start_row_index, start_column_index):
#         return []
#     else:  # if this is a 'legal' starting location
#         current_row_index, current_column_index = start_row_index, start_column_index
#         shortest_path = []
#         shortest_path.append([current_row_index, current_column_index])
#         # continue moving along the path until we reach the goal (i.e., the item packaging location)
#         while not is_terminal_state(current_row_index, current_column_index):
#             # get the best action to take
#             action_index = get_next_action(
#                 current_row_index9, current_column_index, 1.)
#             # move to the next location on the path, and add the new location to the list
#             current_row_index, current_column_index = get_next_location(
#                 current_row_index, current_column_index, action_index)
#             shortest_path.append([current_row_index, current_column_index])
#         return shortest_path


# define training parameters
# the percentage of time when we should take the best action (instead of a random action)
epsilon = 0.7
discount_factor = 0.9  # discount factor for future rewards
learning_rate = 0.5  # the rate at which the agent should learn
# run through 1000 training episodes

solar = pd.read_csv('./solar.txt', names=['data'])

for episode in range(config.EPISODES):
    # get the starting location for this episode

    nodes = []
    edges = []

    for i in range(0, config.NODES):
        nodes.append(Node(i, 0, 0))

    for i in range(0, config.EDGES):
        edges.append(Edge())

    state = get_init_state(0, nodes, edges)
    # continue taking actions (i.e., moving) until we reach a terminal state
    # (i.e., until we reach the item packaging area or crash into an item storage location)
    for i in range(0, int(config.TIME/config.K)):
        # while not is_terminal_state(row_index, column_index):
        # choose which action to take (i.e., where to move next)

        # perform the chosen action, and transition to the next state (i.e., move to the next location)
        # store the old row and column indexes
        # old_row_index, old_column_index = row_index, column_index

        # receive the reward for moving to the new state, and calculate the temporal difference
        random.shuffle(nodes)

        for node in nodes:

            action_index = get_next_action(node.id, state, epsilon)
            edgeIndex, ratio = get_next_location(action_index)

            if node.state == State.ACTIVE:
                if not node.skip:
                    node.sensing()
                    
                    packet = Packet(ratio * node.memory, node.id, i, 0)
                    node.memory = node.memory - packet.data
                    localTime = node.calc_local_processing_time()
                    edgeTime = node.calc_edge_processing_time(
                        edges[edgeIndex], packet)
                    node.realTime += (localTime + edgeTime)

                    edges[edgeIndex].calc_network(packet)

                    node.consume_local_processing_energy()
                    node.consume_send_packet_energy(packet)
                    

                    # print(localTime, edgeTime, node.time)
                    # if(localTime >= 4):
                    #     a = input('').split(" ")[0]
                    # print(node.energy)
                    if max(localTime, edgeTime) <= node.time:
                        node.time = config.K

                    elif localTime > node.time:
                        delayTime = localTime - node.time
                        # print("real delay time: ", delayTime)
                        # a = input('').split(" ")[0]
                        if delayTime >= config.K:
                            node.dropTask += 1
                            node.delayTime += config.K
                            node.skip = True
                            node.time = delayTime
                        else:
                            node.delayTime += delayTime
                            node.time = config.K - delayTime

                    elif edgeTime > node.time:
                        delayTime = edgeTime - node.time
                        if delayTime > config.K:
                            if localTime < edgeTime:
                                node.delayTime += config.K

                        else:
                            if localTime < edgeTime:
                                node.delayTime += (edgeTime - localTime)
                    

                else:
                    delayTime = node.time - config.K
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
            
            old_q_value = q_values[state + (action_index,)]
            state = get_init_state(i, nodes, edges)

            b = 1
            if ratio == 0:
                b = 0

            reward_b = node.dropBlackoutTask - node.beforedropBlackout    
            reward = packet.data - 1 * reward_b - 0.05 * \
                node.energy - 0.1 * max([i.realTime for i in nodes])
            temporal_difference = reward + \
                (discount_factor * np.argmax(q_values[state])) - old_q_value
            # update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (learning_rate * temporal_difference)
            q_values[state + (action_index,)] = new_q_value
            
            if epsilon < 0.01:
                epsilon = 0.01
                continue

            epsilon *= 0.99   
            


        for edge in edges:
            edge.flush()
            

            


    for node in nodes:
        print(node.dropBlackoutTask)
        print(node.realTime)
        print(node.dropTask)
        # print(node.blackoutCount)
        print("\n")
    print("-------------------------------")

print('Training complete!')


temp = [0,0,0,0,0]
for node in nodes:
    temp[0] += node.dropBlackoutTask
    temp[1] += node.realTime
    temp[2] += node.dropTask
    # temp[3] += node.blackoutCount

for i in range(0, len(temp)):
    temp[i] /= config.NODES
    print(temp[i])



# # display a few shortest paths
# print(get_shortest_path(3, 9))  # starting at row 3, column 9
# print(get_shortest_path(5, 0))  # starting at row 5, column 0
# print(get_shortest_path(9, 5))  # starting at row 9, column 5

# # display an example of reversed shortest path
# path = get_shortest_path(5, 2)  # go to row 5, column 2
# path.reverse()
# print(path)
