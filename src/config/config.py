import tomllib
from pathlib import Path

config_path = Path(__file__).parent.parent.parent / "config.toml"
with open(config_path, "rb") as file:
    Config = tomllib.load(file)
