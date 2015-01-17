import json

def get_conf():
    with open('cyrkus.json', 'rb') as j:
        return json.load(j)
