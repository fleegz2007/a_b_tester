import json

class Connector():

    def __init__(self):
        self.details = json.load(open('sampler/configuration/test_config.json'))
