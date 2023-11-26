import numpy as np
import random
from mdp import *
# from notebook import psource, pseudocode, plot_pomdp_utility
# import mdptoolbox
# from mdptoolbox import mdp

class MDP:
    def __init__(self, init, actlist, terminals, transitions = {}, reward = None, states=None, gamma=.9):
        if not (0 < gamma <= 1):
            raise ValueError("An MDP must have 0 < gamma <= 1")
        
        if states:
            self.states = states
        else:
            self.states = self.get_states_from_transitions(transitions)

        self.init = init

        if isinstance(actlist, list):
            self.actlist = actlist
        elif isinstance(actlist, dict):
            self.actlist = actlist
        
        self.terminals = terminals
        self.transitions = transitions
        if self.transitions == {}:
            print("Transition table is empty")
        self.gamma = gamma
        if reward:
            self.reward = reward
        else:
            self.reward = {s : 0 for s in self.states}
    def reward(self, state):
        return self.reward[state]
    def transition(self, state, action):
        if (self.transitions == {}):
            raise ValueError("Transition model is missing")
        else:
            return self.transitions[state][action]
    def actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actlist
    def get_states_from_transitions(self, transitions):
        if isinstance(transitions, dict):
            s1 = set(transitions.keys())
            s2 = set([tr[1] for actions in transitions.values() for effects in actions.values() for tr in effects])
            return s1.union(s2)
        else:
            print('Could not retrieve states from transitions')
            return None
    def check_consistency(self):
        assert set(self.states) == self.get_states_from_transitions(self.transitions)
        assert self.init in self.states
        assert set(self.reward.keys()) == set(self.states)
        assert all([t in self.states for t in self.terminals])
        for s1, actions in self.transitions.items():
            for a in actions.keys():
                s = 0
                for o in actions[a]:
                    s += o[0]
                assert abs(s - 1) < 0.001

class GridMDP(MDP):
    def __init__(self, grid, terminals, init=(0,0), gamma=0.9):
        grid.reverse()
        reward = {}
        states = set()
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = grid
        for x in range(self.cols):
            for y in range(self.rows):
                if grid[y][x] is not None:
                    states.add((x, y))
                    reward[(x, y)] = grid[y][x]
        self.states = states
        actlist = orientations
        transitions = {}
        for s in states:
            transitions[s] = {}
            for a in actlist:
                transitions[s][a] = self.calculate_transition(s, a)
        MDP.__init__(self, init, actlist=actlist, terminals=terminals, transitions=transitions, reward=reward, states=states, gamma=gamma)
    def calculate_transition(self, state, action):
        if action is None:
            return [(0.0, state)]
        else:
            return [(0.8, self.go(state, action)),
                    (0.1, self.go(state, turn_right(action))),
                    (0.1, self.go(state, turn_left(action)))]
    def transition(self, state, action):
        if action is None:
            return [(0.0, state)]
        else:
            return self.transitions[state][action]
    def go(self, state, direction):
        state1 = vector_add(state, direction)
        return state1 if state1 in self.states else state
    def to_grid(self, mapping):
        return list(reversed([[mapping.get((x, y), None) for x in range(self.cols)] for y in range(self.rows)]))
    def to_arrows(self, policy):
        chars = {
            (1, 0): '>', (0, 1): '^', (-1, 0): '<', (0, -1): 'v', None: 'x'}
        return self.to_grid({s: chars[a] for (s, a) in policy.items()})
    
            

# class Environment:
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.goal_x = random.randint(0, width - 1)
#         self.goal_y = random.randint(0, height - 1)
#         self.obstacle_x = random.randint(0, width - 1)
#         self.obstacle_y = random.randint(0, height - 1)
#         print(f"Goal position: ({self.goal_x}, {self.goal_y})")
#     def is_goal_reached(self, x, y):
#         if (x == self.goal_x) and (y == self.goal_y):
#             return 1
#         else:
#             return 0

# # Define the grid size and positions
# env = Environment(10, 10)
# follower_x, follower_y = random.randint(0, env.width-1), random.randint(0, env.height-1)

# # Define rewards and penalties
# rewards = {
#     (env.goal_x, env.goal_y): 10,  # Reward for reaching the goal
#     (env.obstacle_x, env.obstacle_y): -1,  # Penalty for specific obstacles
# }

