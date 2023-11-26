import autogen
import chess
import chess.svg
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

# Load LLM inference endpoints from an env variable or a file
# See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
# and OAI_CONFIG_LIST_sample



config_list = autogen.config_list_from_models(model_list=["gpt-3.5-turbo"])

config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': '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',
    },
]

# assistant = AssistantAgent("assistant", llm_config={"config_list": config_list})
# user_proxy = UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")

# # config_list = autogen.config_list_from_json(
# #     "OAI_CONFIG_LIST",
# #     filter_dict={
# #         "model": ["gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
# #     },
# # )

# llm_config={
#     "request_timeout": 600,
#     "seed": 42,
#     "config_list": config_list,
#     "temperature": 0
# }

from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

sys_msg = """You are an AI-powered chess board agent.
You translate user's natural language input into legal UCI moves.
You should only reply with a UCI move string extracted from user's input."""

class BoardAgentMDP:
    def __init__(self, board: chess.Board):
        self.board = board
        self.correct_move_messages = defaultdict(list)

    def get_possible_actions(self):
        possible_moves = list(self.board.legal_moves)
        return possible_moves
    
    def take_action(self, action):
        self.board.push(action)

    def get_reward(self):
        if self.board.is_checkmate():
            return 1
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0
        else:
            return -1
        
# initial_board = chess.Board()
# agent_mdp = BoardAgentMDP(initial_board)

# while not agent_mdp.board.is_game_over():
#     possible_moves = agent_mdp.get_possible_actions()
#     print(f"Possible moves: {possible_moves}")
#     action = input("Enter your move: ")
#     try:
#         action = chess.Move.from_uci(action)
#     except ValueError as e:
#         print(f"Error: {e}")
#     else:
#         agent_mdp.take_action(action)
#         print(f"Current board:\n{agent_mdp.board}")
#         if agent_mdp.board.is_game_over():
#             break
#         print("AI is thinking...")
#         action = possible_moves[0]
#         agent_mdp.take_action(action)
#         print(f"AI's move: {action}")
#         print(f"Current board:\n{agent_mdp.board}")

# class BoardAgent(autogen.AssistantAgent):
#     board: chess.Board
#     correct_move_messages: Dict[autogen.Agent, List[Dict]]

#     def __init__(self, board: chess.Board):
#         super().__init__(
#             name="BoardAgent",
#             system_message=sys_msg,
#             llm_config={"temperature": 0.0, "config_list": config_list},
#             max_consecutive_auto_reply=10,
#         )
#         self.register_reply(autogen.ConversableAgent, BoardAgent._generate_board_reply)
#         self.board = board
#         self.correct_move_messages = defaultdict(list)

#     def _generate_board_reply(
#         self,
#         messages: Optional[List[Dict]] = None,
#         sender: Optional[autogen.Agent] = None,
#         config: Optional[Any] = None,
#     ) -> Union[str, Dict, None]:
#         message = messages[-1]
#         reply = self.generate_reply(self.correct_move_messages[sender] + [message], sender, exclude=[BoardAgent._generate_board_reply])
#         uci_move = reply if isinstance(reply, str) else str(reply["content"])
#         try:
#             self.board.push_uci(uci_move)
#         except ValueError as e:
#             return True, f"Error: {e}"
#         else:
#             m = chess.Move.from_uci(uci_move)
#             # display(chess.svg.board(self.board, arrows=[(m.from_square, m.to_square)], fill={m.from_square: "gray"}, size=200))
#             self.correct_move_messages[sender].extend([message, self._message_to_dict(uci_move)])
#             return True, uci_move

sys_msg_tmpl = """Your name is {name} and you are a chess player.
You are playing against {opponent_name}.
You are playing as {color}.
You communicate your move using universal chess interface language.
You also chit-chat with your opponent when you communicate a move to light up the mood.
You should make sure both you and the opponent are making legal moves.
Do not apologize for making illegal moves."""

class ChessPlayerAgent(autogen.AssistantAgent):

    def __init__(
        self,
        color: str,
        board_agent: BoardAgentMDP,
        max_turns: int,
        **kwargs,
    ):
        if color not in ["white", "black"]:
            raise ValueError(f"color must be either white or black, but got {color}")
        opponent_color = "black" if color == "white" else "white"
        name = f"Player {color}"
        opponent_name = f"Player {opponent_color}"
        sys_msg = sys_msg_tmpl.format(
            name=name,
            opponent_name=opponent_name,
            color=color,
        )
        super().__init__(
            name=name,
            system_message=sys_msg,
            max_consecutive_auto_reply=max_turns,
            **kwargs,
        )
        self.register_reply(BoardAgentMDP, ChessPlayerAgent._generate_reply_for_board, config=board_agent.board)
        self.register_reply(ChessPlayerAgent, ChessPlayerAgent._generate_reply_for_player, config=board_agent)
        # self.update_max_consecutive_auto_reply(board_agent.max_consecutive_auto_reply(), board_agent)

    def _generate_reply_for_board(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[autogen.Agent] = None,
        config: Optional[chess.Board] = None,
    ) -> Union[str, Dict, None]:
        board = config
        board_state_msg = [{"role": "system", "content": f"Current board:\n{board}"}]
        last_message = messages[-1]
        if last_message["content"].startswith("error"):
            last_message["role"] = "system"
            return True, self.generate_reply(messages + board_state_msg, sender, exclude=[ChessPlayerAgent._generate_reply_for_board])
        else:
            return True, None
        
    def _generate_reply_for_player(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[autogen.Agent] = None,
        config: Optional[BoardAgentMDP] = None,
    ) -> Union[str, Dict, None]:
        board_agent = config
        board_state_msg = [{"role": "system", "content": f"Current board:\n{board_agent.board}"}]
        message = self.generate_reply(messages + board_state_msg, sender, exclude=[ChessPlayerAgent._generate_reply_for_player])
        if message is None:
            return True, None
        self.initiate_chat(board_agent, clear_history=False, message=message, silent=self.human_input_mode == "NEVER")
        last_message = self._oai_messages[board_agent][-1]
        if last_message["role"] == "assistant":
            print(f"{self.name}: I yield.")
            return True, None
        return True, self._oai_messages[board_agent][-2]
    
max_turn = 10
board = chess.Board()
board_agent = BoardAgentMDP(board=board)
player_black = ChessPlayerAgent(
    color="black",
    board_agent=board_agent,
    max_turns = max_turn,
    llm_config={"temperature": 0.5, "seed": 1, "config_list": config_list},
)
player_white = ChessPlayerAgent(
    color="white",
    board_agent=board_agent,
    max_turns=max_turn,
    llm_config={"temperature": 0.5, "seed": 2, "config_list": config_list},
)

player_black.initiate_chat(player_white, message="Your turn.")