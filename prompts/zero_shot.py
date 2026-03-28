# Zero shot prompting

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

# Zero Shot Prompting: Directly  giving the inst to the model
SYSTEM_PROMPT = 'You Should only and only ans the coding related question. do not ans anything else. you name is jarvis. If user asks something other then coding just say sorry'

res =client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role":"system","content":SYSTEM_PROMPT }, # define System content and role of model to bind special content
        {"role":"user", "content":"can you write a python code to translate"}
    ]
)


print(res.choices[0].message.content)

# Zero-shot prompting: the model is given a direct question of task without prior examples.