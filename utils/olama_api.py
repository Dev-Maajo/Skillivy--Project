import os
import requests

# API key from .env file
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_career_roadmap(resume_text, model = "meta-llama/llama-3-8b-instruct"):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": resume_text}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"❌ API Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Exception: {str(e)}"
