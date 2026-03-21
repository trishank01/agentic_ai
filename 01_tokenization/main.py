import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey There! My name is Trishank Khatri"

tokens = enc.encode(text)

print("Tokens", tokens)

encoded = [25216, 3274, 0, 3673, 1308, 382, 1514, 1109, 1104, 658, 13274, 872]

content = enc.decode(encoded)


print("content", content)