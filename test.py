import requests

BASE = "http://127.0.0.1:5000/"
data = [{"likes": 10, "name": "Kung Fury", "views": 100000, },
        {"likes": 10, "name": "Highlights Palmeiras 2020", "views": 80000, },
        {"likes": 35, "name": "Dragon Ball The Movie", "views": 100000, },
        ]
for i in range(0, len(data)):
    response = requests.put(BASE + "video/" + str(i), json=data[i])
    print(response.json())

input()
response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())

