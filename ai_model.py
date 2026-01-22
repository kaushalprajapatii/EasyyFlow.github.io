# ai_model.py
import os
import requests

# Load Hugging Face API Key
HF_API_KEY = os.getenv("HF_API_KEY")
if not HF_API_KEY:
    raise ValueError("HF_API_KEY not found in Streamlit secrets.")

# Hugging Face OpenAI-compatible endpoint
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

def generate_flowchart_steps(topic: str, num_steps: int) -> str:
    print("✅ Using Mistral via Hugging Face (OpenAI-compatible API)")

    prompt = f"""
You must output ONLY plain text.

Generate exactly {num_steps} lines for the topic "{topic}".

STRICT FORMAT (MANDATORY):
Title : Description

RULES:
- Do NOT use numbering (I, II, 1, 2, etc.)
- Do NOT add prefixes or suffixes
- Do NOT repeat the topic name in titles
- Each line must contain exactly ONE colon (:)
- No markdown, no bullets, no extra text
- If formatting is wrong, rewrite until correct

CORRECT EXAMPLE:
Boil Water : Heat water in a kettle until boiling.
Steep Tea : Pour hot water over the tea bag.
Infuse : Let the tea rest for 3 to 5 minutes.
Serve : Remove tea bag and serve hot.

Now generate the output:
"""

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 300
    }

    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"Error: HF API failed ({response.status_code}) - {response.text}"

        data = response.json()
        output = data["choices"][0]["message"]["content"].strip()

        # Final safety cleanup (guarantees format)
        lines = output.split("\n")
        clean_lines = [
            line.strip()
            for line in lines
            if ":" in line and line.count(":") == 1
        ]

        return "\n".join(clean_lines[:num_steps])

    except Exception as e:
        return f"Error: {e}"


















