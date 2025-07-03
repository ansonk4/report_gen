from openai import OpenAI
from dotenv import load_dotenv
import os

class llm:
    def __init__(self, stop_all=True):
        # Read API key from a secret file
        load_dotenv()


        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_KEY"),
        )
        self.stop_all = stop_all

    def generate(self, prompt, output=False):
        if self.stop_all:
            if output is False:
                return "[LLM OUTPUT PLACEHOLDER]"

        completion = self.client.chat.completions.create(
            extra_body={},
            model="mistralai/mistral-small-3.2-24b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt + "ONLY finish the above task WITHOUT any explanation, additional text or markdown."
                        },
                    ]
                }
            ]
        )
        return completion.choices[0].message.content