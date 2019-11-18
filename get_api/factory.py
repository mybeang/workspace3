
import yaml
from pathlib2 import Path
from get_api import *


class Device(object):
    def __init__(self, name):
        self.name = name

    def update_feature(self, **entries):
        self.__dict__.update(entries)


def manufacture(model_name):
    root_path = Path(__file__).parent
    with open(str(root_path.joinpath(model_name)) + ".yaml", 'r') as f:
        data = yaml.load(f)
    device = Device(data['name'])
    device.update_feature(**data['feature'])
    return device


if __name__=="__main__":
    d1 = manufacture("A")
    import pdb
    pdb.set_trace()