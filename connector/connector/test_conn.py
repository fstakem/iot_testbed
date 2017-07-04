
import requests


url = "http://localhost:5000/samples"

data = {
    "sensor_id": "1",
    "sampled_at": "2017-05-20 04:05:25",
    "value": "45"
}
response = requests.post(url, json=data)

print(response.status_code)
print(response.text)
