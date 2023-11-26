import autogen

config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': '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',
    },
]

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    },
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
)

user_proxy.send(
    recipient=assistant,
    message="""Plot a chart of their stock price change YTD and save to stock_price_ytd.png""",
)

from IPython.display import Image

Image(filename='coding/stock_price_ytd.png')