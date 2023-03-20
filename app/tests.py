import requests


BASE = "http://127.0.0.1:5000/"
API_PREFIX = 'api/v0.1/'

response = requests.post(BASE + API_PREFIX + 'data')
print(response.json())
