import jmespath

j = {
    "persons": [
        { "name": "erik", "age": 38 },
        { "name": "john", "age": 45 },
        { "name": "rob", "age": 14 }
    ]
    }

r = jmespath.search("persons[*].age", j)
print(r)
print(type(r))

r = jmespath.search("persons[?name=='erik'].age", j)
print(r)