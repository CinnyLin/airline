data = [
    {"time": "2021/1", "num_tickets": 0},
    {"time": "2021/2", "num_tickets": 0},
    {"time": "2021/3", "num_tickets": 0},
    {"time": "2021/4", "num_tickets": 0}
]

#{"time": "2021/4", "num_tickets": 5}

for monthlyDict in data:
    for key, value in monthlyDict.items():
        if (key=="time") and (value=="2021/4"):
            monthlyDict["num_tickets"]=5

print(data)