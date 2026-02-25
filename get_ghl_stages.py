import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(
    "https://rest.gohighlevel.com/v1/pipelines/",
    headers={"Authorization": "Bearer ed9671f8-525e-4fd4-9c40-045a0b2fde08"}
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        with open("pipeline_data.json", "w") as f:
            json.dump(data, f, indent=4)
except Exception as e:
    with open("pipeline_data.json", "w") as f:
        f.write(str(e))
