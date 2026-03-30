# Chain of thought

from dotenv import load_dotenv
from openai import OpenAI
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
import os
load_dotenv()

# Agentic_Ai_practice

client = OpenAI()

def run_command(cmd:str):
    result = os.system(cmd)
    return result

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    
    return "Something went wrong"


available_tool = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.
    You can also call a tool if required from the list of available tools.
    for every tool call wait for observe step which is the output from the called tool


    Rules:
    - Stricitly Follow The given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (WHich is going to the displayed the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT" | "TOOL" , "content:"string" , "tool": "string", "input":"string"}'

    Available Tools:
    - get_weather: Takes city name as an input string and return the weather info about the city
    - run_command: this tool help you create file in user system use it when need to create file or folder


    Example 1:
    START: Hey. Can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in Math problem"}
    PLAN: {"step:  "PLAN", "content": "looking at the problem, we should solve this problem using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "first we must multiple 3*5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5" }
    PLAN: {"step": "PlAN", "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now Finally lets perform the add 3.5 as ans"}
    PLAN: {"step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as answer"}
    OUTPUT:{"step": "OUTPUT", "content":"3.5"}

    Example 2:
    START: What is the weather of Delhi?
    PLAN: {"step": "PLAN", "content": "Seems like user is interested in getting weather of delhi in india"}
    PLAN: {"step:  "PLAN", "content": "lets see if we have any available tool from the list of available tools"}
    PLAN: {"step": "PLAN", "content": "Great, wh have get_weather tool available for this query"}
    PLAN: {"step": "PLAN", "content": "I need to call get_weather tool for for delhi as input for city"}
    PLAN: {"step": "TOOL", tool: "get_weather", "input": "delhi" }
    PLAN: {"step": "OBSERVE", tool: "get_weather",  "content": "The temp of delhi is cloudy with 20 C"}
    PLAN: {"step": "PLAN", "content": "I got the weather info about"}
    OUTPUT:{"step": "OUTPUT", "content":"The current weather in delhi is 20 c with cloudy sky"}
 """
print("\n\n\n")

class MyOutputFormat(BaseModel):
    step: str = Field(... , description="The ID of the step. Example: PLAN, OUTPUT, TOOL, etc")
    content: Optional[str] = Field(None, description="The optional string content for the step")
    tool: Optional[str] = Field(None, description="The ID of the tool to call")
    input : Optional[str] = Field(None, description="The input params for the tool")



message_history = [
{"role": "system", "content": SYSTEM_PROMPT}
 ]

while True:
    user_query = input("-> ")
      # Optional: A way to exit the loop
    if user_query.strip().lower() in ['quit', 'exit']:
        print("Goodbye!")
        break
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
        model='gpt-4o-mini',
        response_format=MyOutputFormat,
        messages=message_history
    )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant","content":raw_result}),

        parsed_result = response.choices[0].message.parsed


        if parsed_result.step == "START":
            print("starting LLM loop", parsed_result.content)
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            print(f"starting with tool ->  {tool_to_call} {tool_input}")
            tool_response = available_tool[tool_to_call](tool_input)
            print(f"starting with tool res ->  {tool_to_call} {tool_input} = {tool_response}")
            message_history.append({"role":"assistant", "content": json.dumps(
            {  "step":"OBSERVE", "tool":tool_to_call, "input":tool_input, "output": tool_response}
            )})
            continue
        
        
        if parsed_result.step == "PLAN":
            print("PLAN started", parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("OUTPUT", parsed_result.content)
            break



print("\n\n\n")


# can you solve math problme 300 - 20 * 3 / 10 - 5
