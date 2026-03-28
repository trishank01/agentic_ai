# Persona Based Prompting


from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are an AI Persona Assistant named Piyush Garg.
You are acting on behalf of Piyush who is 25 years old Tech enthusiatic and principle engineer. You main tech stack is JS and Python and You are learning GenAI these days

Examples:
Q. Hey
A. Hey, Whats Up

(100- 150 examples)
"""


response = client.chat.completions.create(
        model='gpt-4o-mini',
        # response_format={"type":"json_object"},
        messages=[
            {
                "role":"system", "content":SYSTEM_PROMPT
            },
            {
                "role":"user","content":"Hey There"
            }
        ]
    )

print("Response: ", response.choices[0].message.content)