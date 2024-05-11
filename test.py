import requests

BASE = "http://127.0.0.1:5000/"

response = requests.patch(BASE + "video/2", {"views":99, "likes":70})
print(response.json())
# data = [{"likes": 10, "name": "Kung Fury", "views": 100000},
#         {"likes": 10, "name": "Highlights Palmeiras 2020", "views": 80000},
#         {"likes": 35, "name": "Dragon Ball The Movie", "views": 2000}]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), json=data[i])
#     print(response.json())
#
#     input()
#     response = requests.get(BASE + "video/6")
#     print(response.json())


    # try:
    #     print(response.json())
    # except Exception as e:
    #     print("Error:", e)
