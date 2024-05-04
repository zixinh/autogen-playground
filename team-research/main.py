import os

import autogen
import openai

llm_config = {
    "config_list": [
        {
            "model": os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
            "api_type": "azure",
            "api_key": os.environ["AZURE_OPENAI_API_KEY"],
            "base_url": os.environ["AZURE_OPENAI_API_ENDPOINT"],
            "api_version": os.environ["AZURE_OPENAI_API_VERSION"]
        },
        {
            "model": "gpt-4",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    ],
    "timeout": 300
}


