# Chain of thought

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thoughts.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.


    Rules:
    - Stricitly Follow The given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (WHich is going to the displayed the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT" , "content:"string" }

    Example:
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
 """
print("\n\n\n")


message_history = [
{"role": "system", "content": SYSTEM_PROMPT}
 ]

user_query = input("-> ")
message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant","content":raw_result}),

    parsed_result = json.loads(raw_result)

    if parsed_result.get("step") == "START":
        print("starting LLM loop", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step") == "PLAN":
        print("PLAN started", parsed_result.get("content"))
        continue

    if parsed_result.get("step") == "OUTPUT":
        print("OUTPUT", parsed_result.get("content"))
        break

print("\n\n\n")


# can you solve math problme 300 - 20 * 3 / 10 - 5
