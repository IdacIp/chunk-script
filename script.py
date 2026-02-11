import requests
import base64
import os
import json

# Set up machine and get the credentials from https://huggingface.co/openai/whisper-large-v3-turbo -> HF Inference
# change audio format to .flac before running the script, and put the files in the "audio" folder

def query(payload):
 headers = {
  "Accept" : "application/json",
  "Authorization": "Bearer " + str(os.getenv("HF_TOKEN")),
  "Content-Type": "application/json"
 }
 response = requests.post(
  os.getenv("HF_INFERENCE_ENDPOINT"),
  headers=headers,
  json=payload
 )
 return response.json()

folder = "audio"
flac_files = [f for f in os.listdir(folder) if f.lower().endswith(".flac")]

results = []
for fname in flac_files:
    print(f"Processing file: {fname}")
    path = os.path.join(folder, fname)
    with open(path, "rb") as f:
        base_64_encoded = base64.b64encode(f.read())
        base_64_str = base_64_encoded.decode('utf-8')

    output = query({
     "inputs": base_64_str,
     "parameters": {}
    })
    print(f"Successfully converted {fname} to text.")
    results.append((fname, output))

# Print results in Markdown format
for fname, output in results:
    print(f"## {fname}\n")
    print("```json")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("```\n")
