import json

jsonstring = '{"name": "erik", "age": 38, "married": true}'
person = json.loads(jsonstring)
print(person['name'], 'is', person['age'], 'years old')
print(person)

d = json.dumps(person, indent=2)
print(d)
print(type(d))

# Read a JSON file
with open('data.json') as json_file:
    data = json.load(json_file)
    
# Write JSON to a file
data = {'name': 'Eric', 'age': 38 }
with open('data.json', 'w') as json_file:
    json.dump(data, json_file)