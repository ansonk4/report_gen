import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from google import genai

class llm:
    def __init__(self, google=False, stop_all=False, max_retries=2, backoff=15):
        load_dotenv()

        if google:
            self.client = genai.Client()
        else:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_KEY"),
            )

        self.google = google
        self.stop_all = stop_all
        self.max_retries = max_retries      # total attempts (first + retries)
        self.backoff = backoff              # seconds to wait before each retry

    def generate(self, prompt, output=False):
        # Return placeholder immediately if we're short‑circuiting
        if self.stop_all and output is False:
            return "[LLM OUTPUT PLACEHOLDER]"

        attempt = 0
        while attempt < self.max_retries:
            try:
                if self.google:
                    resp = self.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt + "ONLY finish the above task WITHOUT any explanation, additional text or markdown."
                    )
                    return resp.text
                else:
                    resp = self.client.chat.completions.create(
                        model="mistralai/mistral-small-3.2-24b-instruct:free",
                        messages=[{
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt + "ONLY finish the above task WITHOUT any explanation, additional text or markdown."
                                }
                            ]
                        }],
                    )
                    return resp.choices[0].message.content

            except Exception as e:
                attempt += 1
                if attempt >= self.max_retries:
                    # Give up after last retry
                    print(f"LLM call failed after {self.max_retries} attempts: {e}")
                    return "[LLM OUTPUT PLACEHOLDER]"
                time.sleep(self.backoff * attempt)  # simple exponential back‑off


if __name__ == "__main__":
    llm = llm(google=True)
    print(llm.generate("Explain how AI works in a few words"))