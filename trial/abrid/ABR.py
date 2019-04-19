from .AbrInterface import AbrBase
import json


def load_json(path):
    with open(path) as file:
        obj = json.load(file)
    return obj


class Abr(AbrBase):

    def __init__(self, config):
        self.bitrate_count = config['bitrate_count']
        self.bitrate_list = config['bitrate_list']

    def get_first_quality(self):
        return 0

    # def get_quality




if __name__ == '__main__':
    config_obj = load_json('config_req.json')
    abr = Abr(config_obj)
    a = 'debug'
