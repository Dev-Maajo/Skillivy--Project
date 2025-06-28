import os
import requests

# Env se OpenRouter key lena
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_feedback(resume_text):
    try:
        prompt = f"""
You are an expert career counselor and resume reviewer.
Read the following resume content and provide clear, concise, and constructive feedback in bullet points:

--- Resume Start ---
{resume_text}
--- Resume End ---

Your feedback should cover: formatting, grammar, clarity, and suggestions to improve.
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",  # Or any other model like anthropic/claude
                "messages": [
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            }
        )

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content'].strip()
        else:
            return f"❌ Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Exception: {str(e)}"
