import os

import autogen
import openai

config_list = [
    {
        "model": os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        "api_type": "azure",
        "api_key": os.environ["AZURE_OPENAI_API_KEY"],
        "base_url": os.environ["AZURE_OPENAI_API_ENDPOINT"],
        "api_version": os.environ["AZURE_OPENAI_API_VERSION"]
    },
    # {
    #     "model": "gpt-4",
    #     "api_key": os.environ["OPENAI_API_KEY"]
    # }
]



llm_config = {
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
    code_execution_config=False
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Engineer. You follow with an approved plan. You write python/shell code to solve tasks. 
        Wrap the code in a code block that specifies the script type. Don't use a code block if it's not intended to be executed by the executor.
        The user can't modify your code, so do not suggest incomplete code which requires others to modify.
        Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. 
        If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumptions, collect additional info you need, and think of a different approach to try.
        """
)

scientist = autogen.AssistantAgent(
    name="Scientist",
    llm_config = llm_config,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after  seeing their abstracts printed. You don't write code."""
)

planner = autogen.AssistantAgent(
    name="Planner",
    llm_config=llm_config,
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
    The plan may involve an engineer who can write code and a scientist who doesn't write code.
    Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
    """
)

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "paper",
        "use_docker": True,
    }
)

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""Critic. Double check plan, claims, code from other agents and provide feedback.
     Check whether the plan includes adding verifiable info such as source URL.
    """
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, scientist, planner, executor, critic],
    messages=[],
    max_round=50
)

manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# planner and critic is a pair, admin will approve the plan
# engineer and scientist is a pair, executor is engineer's helper to execute the code
# for any question from user_proxy, planner will make a plan, critic will double check the plan, and admin will approve the plan
# engineer and scientist would follow the plan while executor is the helper to execute the code
# after certain rounds of conversation between engineer and scientist, critic will double check the plan, and admin will approve the plan
# until the result is good enough for critic and return to user_proxy