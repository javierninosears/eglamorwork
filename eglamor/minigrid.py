import gym
import numpy as np
import autogen
import minigrid
# import gym_minigrid
# from gym_minigrid import EmptyEnv

# envs = gym.envs.registry.keys()
# print(envs)

config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': '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',
    },
]

class LeaderAgent(autogen.AssistantAgent):
    def __init__(self, agent, env):
        self.agent = agent
        self.assistance_agent = autogen.AssistantAgent(
            name="leader",
            system_message="You are an assistant agent acting as the 'Leader', and your role is to navigate a 'Follower' LLM agent\
                through the MiniGrid environment specified by the variable 'minigrid_env'.\
                The state of the 'minigrid_env' variable can be retrieved with the 'get_minigrid_state' function.\
                    Your job is to analyze this state and provide instructions to the 'FollowerAgent' LLM agent with regards to where it should move next.\
                        You can provide instructions to the 'FollowerAgent' LLM agent by using the 'send_message' function.\
                            The 'send_message' function takes in a string as an argument, and this string should be one of the following:\
                                'left', 'right', 'forward', 'pickup', 'drop', 'toggle', 'done'. 'left' corresponds to the action of\
                                    'Turn left', 'right' corresponds to the action of 'Turn right', 'forward' corresponds to the action of 'Move forward', 'pickup' corresponds to\
                                        the action of 'Pick up an object', 'drop' corresponds to the action of 'Drop an object', 'toggle' corresponds to the action of 'Open a door',\
                                            and 'done' corresponds to the action of 'Finish the task'. You can also use the command 'help' to see this message again.",
            llm_config={
                "seed": 42,
                "config_list": config_list,
                "temperature": 0,
            },
            max_consecutive_auto_reply=100,
        )
        self.env = minigrid_env
    
    def get_minigrid_state(self):
        return self.env.grid.encode()
    
    def find_best_response(self, state):
        state = self.get_minigrid_state()



    def send_message(self, message):
        return self.agent.send_message(message)
    

class FollowerAgent(autogen.AssistantAgent):
    def __init__(self, agent, env):
        self.agent = agent
        self.assistance_agent = autogen.AssistantAgent(
            name="follower",
            system_message="You are an assistant agent acting as the 'Follower', and your role is to navigate\
                through the MiniGrid environment specified by the variable 'minigrid_env' using instructions provided by the 'Leader' LLM agent.\
                    You should retrieve the message from the 'LeaderAgent', and then alter the 'minigrid_env' variable by taking one of several steps:\
                        'left', 'right', 'forward', 'pickup', 'drop', 'toggle', 'done'. 'left' corresponds to the action of\
                            'Turn left', 'right' corresponds to the action of 'Turn right', 'forward' corresponds to the action of 'Move forward', 'pickup' corresponds to\
                                the action of 'Pick up an object', 'drop' corresponds to the action of 'Drop an object', 'toggle' corresponds to the action of 'Open a door',\
                                    and 'done' corresponds to the action of 'Finish the task'. You can also use the command 'help' to see this message again.",
            llm_config={
                "seed": 42,
                "config_list": config_list,
                "temperature": 0,
            },
        )
        self.env = minigrid_env
    
    def receive_message(self):
        return self.agent.receive(str, LeaderAgent)
    
    def update_minigrid(self):
        action = self.receive_message()
        obs, reward, done, info = self.env.step(action)
        return obs

    def send_message(self, message):
        message = self.update_minigrid()
        return self.agent.send_message(message, LeaderAgent)


minigrid_env = gym.make('MiniGrid-Empty-8x8-v0')

num_episodes = 10

agent1 = LeaderAgent(autogen.AssistantAgent, minigrid_env)
agent2 = FollowerAgent(autogen.AssistantAgent, minigrid_env)

agent1.initiate_chat(agent2)





