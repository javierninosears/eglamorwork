# simple assistance game
# goal is to navigate through a grid to a goal set of coordinates

import random
import autogen
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

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

config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': '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',
    },
]

sys_msg = """You are an AI-powered assistance agent. Your goal is to assist 
the user in navigating through a grid to a goal set of coordinates. You should
only reply with a direction string extracted from user's input."""

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    },
)

# class AssistanceAgent(autogen.AssistantAgent):
#     def __init__(self):
#         self.assistance_agent = assistant
#         # self.register_reply(AssistanceAgent, PlayerAgent._generate_reply_for_assistant, config=AssistanceAgent)
#         # self.register_reply(PlayerAgent, PlayerAgent._generate_reply_for_player, config=AssistanceAgent)

    # def _generate_reply_for_assistant(self, message: Dict[str, Any]) -> str:
    #     if self.turns >= self.max_turns:
    #         return "TERMINATE"
    #     else:
    #         self.turns += 1
    #         return self.assistance_agent.assist(self.player_x, self.player_y, env.goal_x, env.goal_y)
    # def assist(self, player_x, player_y, goal_x, goal_y):
    #     if player_x < goal_x:
    #         return "Move right"
    #     elif player_x > goal_x:
    #         return "Move left"
    #     elif player_y < goal_y:
    #         return "Move up"
    #     elif player_y > goal_y:
    #         return "Move down"
    #     else:
    #         return "You've reached the goal!"

sys_msg_tmpl = """You are an AI-powered user proxy agent. Your goal is to understand
directions from the assistance agent with the end goal of navigating to a goal
position in a grid. You should react to the instruction given to you by the
assistance agent and move accordingly."""

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    # llm_config = {
    #     "seed": 42,
    #     "config_list": config_list,
    #     "temperature": 0,
    # },
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)
        
# class PlayerAgent(autogen.AssistantAgent):
#     def __init__(self):
#         self.player_x = random.randint(0, env.width - 1)
#         self.player_y = random.randint(0, env.height - 1)
#         self.player_agent = user_proxy
#         # self.register_reply(AssistanceAgent, PlayerAgent._generate_reply_for_assistant, config=PlayerAgent)
#         # self.register_reply(PlayerAgent, PlayerAgent._generate_reply_for_player, config=PlayerAgent)
#     def _generate_reply_for_assistant(self, message: Dict[str, Any]) -> str:
#         if self.turns >= self.max_turns:
#             return "TERMINATE"
#         else:
#             self.turns += 1
#             return self.player_agent.take_action(self.player_x, self.player_y, env.goal_x, env.goal_y)
#     def take_action(self, assistance_agent, env):
#         print(f"Player's position: ({self.player_x}, {self.player_y})")

#         assist_message = assistance_agent.assist(self.player_x, self.player_y, env.goal_x, env.goal_y)
#         print(f"Assistance Agent says: {assist_message}")
#         if assist_message == "Move right":
#             self.player_x += 1
#         elif assist_message == "Move left":
#             self.player_x -= 1
#         elif assist_message == "Move up":
#             self.player_y += 1
#         elif assist_message == "Move down":
#             self.player_y -= 1

#         if env.is_goal_reached(self.player_x, self.player_y):
#             print(f"Player's position: ({self.player_x}, {self.player_y})")
#             print("Congratulations! Goal reached.")
#         else:
#             print("Goal not reached yet.")
#             self.take_action(assistance_agent, env)


width, height = 10, 10
env = Environment(width, height)
starting_loc_x, starting_loc_y = random.randint(0, width - 1), random.randint(0, height - 1)
print(f"Starting location: ({starting_loc_x}, {starting_loc_y})")

user_proxy.initiate_chat(
    assistant,
    message=f"""Given the environment specified by the variable name "env",
    where should I move to reach my goal? Assume I can only move
    one space at a time. My starting location is {starting_loc_x}
    as the x-coord and {starting_loc_y} as the y-coord.
    The goal coordinates are {env.goal_x} as the x-coord and
    {env.goal_y} as the y-coord."""
    )
