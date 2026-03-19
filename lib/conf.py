import json

from .asset_path import ASSET_PATH

with open(ASSET_PATH + "conf.json") as j:
    conf = json.loads(j.read())
