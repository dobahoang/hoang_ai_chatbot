import json
# Environment Variables
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

user_query = "What services do you provide?"


def get_services():
    """Get all available services """
    print("log get hard code array services")
    services_info = {
        "services": ["General cleaning", "Specialized cleaning"],
    }
    print(services_info)
    return json.dumps(services_info)


def get_response(user_query):
    """Get the response from the chat"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {"role": "user", "content": user_query},
            {
                "role": "function",
                "name": "get_services",
                "content": get_services(),
            },
        ],
    )
    return response.__getattribute__("choices")[0].__getattribute__("message").content

