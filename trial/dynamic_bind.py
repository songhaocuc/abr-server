import importlib


AbrId = 'abrid'
AbrFilename = 'ABR'
AbrClass = 'Abr'
AbrModule = importlib.import_module('.', AbrId + '.' + AbrFilename)
Abr = getattr(AbrModule, AbrClass)


if __name__ == '__main__':
    import json


    def load_json(path):
        with open(path) as file:
            obj = json.load(file)
        return obj


    config_obj = load_json('config_req.json')
    abr = Abr(config_obj)
    a = 'debug'
