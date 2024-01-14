from openai import OpenAI
import json

client = OpenAI()

def get_services():
    services=  ["General cleaning", "Specialized cleaning"]
    return json.dumps({"services": services})

def run_conversation(content):
    print("log get hard code array services")

    messages = [{"role": "user", "content": "What services do you provide?"}]
    print(messages)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_services",
                "description": "get services that company provide",

            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:

        available_functions = {
            "get_services": get_services,
        }
        messages.append(response_message)  # extend conversation with assistant's reply
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call()
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response.__getattribute__("choices")[0].__getattribute__("message").content
# print(run_conversation(content))