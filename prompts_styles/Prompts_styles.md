# Prompts styles

SYSTEM_PROMOT = "hey write a code to add 2 + 3"

## Alpaca Prompt

### Instructions: 
<SYSTEM_PROMOT>\n

### Input: <USER_QUERY>

### Response:\n

# CHATML
{
    "role":"system" | "user" | "assistant"
    "content":"string"
}

# INST Prompting
[INST] what is the time? [/INST]


