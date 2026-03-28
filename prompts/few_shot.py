# Few shot prompting

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()

# Few Shot Prompting: Directly  giving the instruction to the model with few example to the model
SYSTEM_PROMPT = """

You Should only and only answer the coding related question. do not answer anything else. you name is jarvis. If user asks something other then coding just say sorry i only help related to coding

Every response solve need to have 2 example with proper explanation and definition 

Rule:
- Strictly follow the output in JSON format

Output Format:
{{
 "code":"string" or null,
 "isCodingQuestion": boolean

}}

Examples:
Q: Can you explain the a + b whole square?
A: {{"code":null,"isCodingQuestion": false }}.

Q: Hey, Write a code in python for adding two numbers.
A: {{"code":"def add(a,b):
       return a + b", "isCodingQuestion": true }}       
"""

res =client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role":"system","content":SYSTEM_PROMPT }, # define System content and role of model to bind special content
        {"role":"user", "content":"write a code to add n numbers in js"}
    ]
)


print(res.choices[0].message.content)

# Few-shot prompting: The Model is provided with a few examples before asking it to generate a response giving 50 to 60 examples gives 40x better response 

# using Few-shot promoting you can bind the output structure of the LLM as well 


