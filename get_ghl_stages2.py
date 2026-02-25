import requests
import json

api_key = "ed9671f8-525e-4fd4-9c40-045a0b2fde08"
pipeline_id = "DKYzvyWdZsd016AkO1gi"

url = "https://rest.gohighlevel.com/v1/pipelines/"
headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    
    with open("c:\\Users\\pruth\\OneDrive\\Desktop\\AI-Automation-System\\pipeline_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
except Exception as e:
    with open("c:\\Users\\pruth\\OneDrive\\Desktop\\AI-Automation-System\\pipeline_error.txt", "w", encoding="utf-8") as f:
        f.write(str(e))
