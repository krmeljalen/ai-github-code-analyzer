import os
import yaml

root_dir = os.path.dirname(os.path.abspath(__file__))

with open(f"{root_dir}/../config.yaml", "r") as file:
    config = yaml.safe_load(file)
