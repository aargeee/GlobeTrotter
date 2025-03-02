import requests
import json
import os

ARLIAI_API_KEY = os.environ.get("ARLIAI_API_KEY")

url = "https://api.arliai.com/v1/chat/completions"

payload = json.dumps({
  "model": "Mistral-Nemo-12B-Instruct-2407",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi!, how can I help you today?"},
    {"role": "user", "content": "Say hello!"}
  ],
  "repetition_penalty": 1.1,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_tokens": 1024,
  "stream": False
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': f"Bearer {ARLIAI_API_KEY}"
}

response = requests.request("POST", url, headers=headers, data=payload)