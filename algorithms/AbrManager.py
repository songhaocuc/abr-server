import importlib
import uuid
import json
import os

# 动态获取abr类
def dynamic_bind(abr_id, exec_filename, abr_class):
    abr_module = importlib.import_module('.', abr_id + '.' + exec_filename)
    abr = getattr(abr_module, abr_class)
    return abr


def get_instance_id():
    return str(uuid.uuid1())


def load_json(path):
    with open(path) as file:
        obj = json.load(file)
    return obj


class AbrManager:

    def __init__(self):
        self.abr_instances = {}

    def init_abr(self, abr_id, config_massage):
        print('abr_id: ' + abr_id + '\n')
        print('config: ' + config_massage + '\n')
        config = json.loads(config_massage)
        path1 = os.path.dirname(__file__)  # debug
        config = load_json(os.path.join(path1, 'config_req.json'))  # debug
        abr_class = dynamic_bind(abr_id, 'ABR', 'Abr')
        abr_instance = abr_class(config)
        instance_id = get_instance_id()
        self.abr_instances[instance_id] = abr_instance
        return instance_id.__str__()

    def exec_abr(self, instance_id, state_message):
        abr_instance = self.abr_instances[instance_id]
        state = json.loads(state_message)
        # abr_instance.
        print('run ' + instance_id)
        return 'abr_result: ' + instance_id

    def clear_abr(self, instance_id):
        abr_instance = self.abr_instances.pop(instance_id)
        del abr_instance
        return 'clear: ' + instance_id

