import json

class Conf(object):
    """
    Configuration object, access values as conf["key"]
    """
    data = None

    def __init__(self):
        pass

    def __getitem__(self, key):
        return self.data[key]

    def __getattr__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def load(self, conf_file):
        with open(conf_file) as json_data_file:
            self.data = json.load(json_data_file)

conf = Conf()
