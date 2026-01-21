import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "mistral",
    "prompt": "Explain flowcharts in very simple words",
    "stream": False
}

response = requests.post(url, json=payload)

data = response.json()
print(data["response"])
