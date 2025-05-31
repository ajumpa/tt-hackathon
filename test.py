import os

from openai import OpenAI
#https://established-ricky-nayadaur-9d9bb87f.koyeb.app/ 
client = OpenAI(
  api_key = os.environ.get("OPENAI_API_KEY", "fake"),
  base_url="https://established-ricky-nayadaur-9d9bb87f.app/v1",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Tell me a joke.",
        }
    ],
    model="meta-llama/Llama-3.1-8B-Instruct",
    max_tokens=30,
)

print(chat_completion.to_json(indent=4))