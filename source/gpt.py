import openai
import os
from dotenv import load_dotenv

def write(message):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_KEY")

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return response