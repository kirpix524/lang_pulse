import json

CONFIG_PATH = "settings.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

USERS_DB_FILE = config["users_db_file"]
LOGS_DIRECTORY = config["logs_directory"]