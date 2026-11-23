import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse 
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
import json
import sys



parser = argparse.ArgumentParser(description="chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


try:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY") 
except: 
    raise RuntimeError("No api key found")

client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = api_key,
) 


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt}
]

for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        tools = available_functions,
    )


    if args.verbose: 
        if response.usage:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}") 
        else: 
            raise RuntimeError("cannot get the usage object")

    ai_message = response.choices[0].message 

    if ai_message.tool_calls: 
        for tool_call in ai_message.tool_calls: 
            function_args = json.loads(tool_call.function.arguments or "{}")
            #print(f"Calling fucntion: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, args.verbose)

            if not result_message["content"]: 
                raise Exception("The 'call_function' function did not returned any content")
            elif args.verbose: 
                print(f"-> {result_message['content']}")

    else: 
        print("Final response: ")
        print(ai_message.content)
        sys.exit(0)
    # print("Response:")
    # print(response.choices[0].message.content)

    messages.append(ai_message)
    messages.append(result_message)


sys.exit(1)
