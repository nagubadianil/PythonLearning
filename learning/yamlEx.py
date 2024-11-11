import yaml

with open('config.yaml','r') as file:
    prime_service = yaml.safe_load(file)

print(prime_service)
print(prime_service['rest']['url'])

import yaml

names_yaml = """
- 'eric'
- 'justin'
- 'mary-kate'
"""

names = yaml.safe_load(names_yaml)

with open('names.yaml', 'w') as file:
    yaml.dump(names, file)

print(open('names.yaml').read())