import sys
import os

os.system("pip install -q -U g4f curl_cffi nest_asyncio")

import g4f
from g4f.client import Client

def test():
    client = Client()
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Extract ASL sign keywords from this sentence: I want to learn advanced calculus. Return ONLY comma separated keywords."}],
        )
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
