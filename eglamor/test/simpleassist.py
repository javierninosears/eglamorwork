# simple assistance game
# goal is to navigate through a grid to a goal set of coordinates

import random
# import autogen

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.goal_x = random.randint(0, width - 1)
        self.goal_y = random.randint(0, height - 1)
        print(f"Goal position: ({self.goal_x}, {self.goal_y})")
    def is_goal_reached(self, x, y):
        if (x == self.goal_x) and (y == self.goal_y):
            return 1
        else:
            return 0

class AssistanceAgent:
    def assist(self, player_x, player_y, goal_x, goal_y):
        if player_x < goal_x:
            return "Move right"
        elif player_x > goal_x:
            return "Move left"
        elif player_y < goal_y:
            return "Move up"
        elif player_y > goal_y:
            return "Move down"
        else:
            return "You've reached the goal!"
        
class PlayerAgent:
    def __init__(self):
        self.player_x = random.randint(0, env.width - 1)
        self.player_y = random.randint(0, env.height - 1)
    def take_action(self, assistance_agent, env):
        print(f"Player's position: ({self.player_x}, {self.player_y})")

        assist_message = assistance_agent.assist(self.player_x, self.player_y, env.goal_x, env.goal_y)
        print(f"Assistance Agent says: {assist_message}")
        if assist_message == "Move right":
            self.player_x += 1
        elif assist_message == "Move left":
            self.player_x -= 1
        elif assist_message == "Move up":
            self.player_y += 1
        elif assist_message == "Move down":
            self.player_y -= 1

        if env.is_goal_reached(self.player_x, self.player_y):
            print(f"Player's position: ({self.player_x}, {self.player_y})")
            print("Congratulations! Goal reached.")
        else:
            print("Goal not reached yet.")
            self.take_action(assistance_agent, env)


width, height = 10, 10
env = Environment(width, height)
assistance_agent = AssistanceAgent()
player_agent = PlayerAgent()

player_agent.take_action(assistance_agent, env)