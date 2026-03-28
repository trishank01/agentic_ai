from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI()


res =client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role":"system","content":"You are an export in Maths and only and only ans maths related questions. if question is not related to Math dont ans it and say Sorry, I only answer math-related question"},  # define System content and role of model to bind special content
        {"role":"user", "content":"hey can you help me to solve a + b whole qube"}
    ]
)


print(res.choices[0].message.content)