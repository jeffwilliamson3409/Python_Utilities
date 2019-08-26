d = [{'x':1, 'y':2}, {'x':3, 'y':4}]

def add_em(myDict):
    return myDict['x'] + myDict['y']

result = map(add_em, d)

for i in result:
    print(i)