import json
import os

class ConfigError(Exception):
    pass

def load_config(file_path="db/config.json"):
    if not os.path.exists(file_path):
        raise ConfigError("Config File Not Found")

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            raise ConfigError("Invalid Config File")

    required_keys = ["user", "password", "host", "port", "service_name"]
    for key in required_keys:
        if key not in config:
            raise ConfigError(f"Missing required parameter '{key}' in config file.")

    if not isinstance(config["port"], int) or config["port"] <= 0:
        raise ConfigError("Port must have a positive integer.")

    for key in ["user", "password", "host", "service_name"]:
        if not isinstance(config[key], str) or not config[key].strip():
            raise ConfigError(f"{key} must not be a non-empty string.")

    return config