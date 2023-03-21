import requests
import sys
url = ""
stat = 0
if len(sys.argv) > 1:
    url = str(sys.argv[2])
    stat = int(sys.argv[1])
else:
    url = 'http://127.0.0.1:5000/'
    stat = 1
Headers = { "ngrok-skip-browser-warning" : "100" }
x = requests.post(url, json = {'status' : stat},headers=Headers)
print(x.json())