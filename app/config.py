import json
from enum import Enum

CONFIG_PATH = "settings.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)
LAYOUTS_DIRECTORY = config["layouts_directory"]
FILE_NAMES = {"USERS": config["users_db_file"],
              "LANGUAGES": config["languages_db_file"],
              "WORDS": config["words_db_file"]}
DICTIONARY_DATA = {"DIRECTORY": config["dictionaries_directory"],
                   "FILE_NAME_PREFIX": config["dictionaries_file_name_prefix"]}
SESSIONS_DATA = {"DIRECTORY": config["sessions_directory"],
                "FILE_NAME_PREFIX": config["sessions_file_name_prefix"]}
STATS_DATA = {"DIRECTORY": config["stats_directory"],
              "FILE_NAME_PREFIX": config["stats_file_name_prefix"]}

WORD_REPO_DATA = {"DIRECTORY": config["words_directory"],
                  "FILE_NAME_PREFIX": config["words_file_name_prefix"]}

SQL_DATA = {
    "db_path": config["sqlite_database"],
    "word_repo_table_prefix": config["words_sql_table_prefix"],
    "users_table_name": config["users_sql_table"],
    "languages_table_name": config["languages_sql_table"],
    "user_dictionary_table_prefix": config["user_dictionary_sql_table_prefix"],
    "sessions_table_prefix": config["sessions_sql_table_prefix"],
    "trainings_table_prefix": config["trainings_sql_table_prefix"],
    "session_words_table_prefix": config["session_words_sql_table_prefix"],
}

TRAINING_DIRECTIONS = config.get("training_directions", [])
TrainingDirection = Enum("TrainingDirection", {name.upper(): name for name in TRAINING_DIRECTIONS})
def get_direction_name(direction: TrainingDirection) -> str:
    if direction:
        return config["training_directions_names"].get(direction.value, direction.value)
    else:
        return ""

LOGS_DIRECTORY = config["logs_directory"]
SCREEN_WIDTH = config["screen_settings"]["width"]
SCREEN_HEIGHT = config["screen_settings"]["height"]




LOGIN_SCREEN_CHOOSE_USER_TEXT = config["login_screen_settings"]["choose_user_spinner_text"]
LOGIN_SCREEN_LOGIN_BUTTON_TEXT = config["login_screen_settings"]["login_button_text"]
LOGIN_SCREEN_REGISTER_BUTTON_TEXT = config["login_screen_settings"]["register_button_text"]
REGISTER_SCREEN_USER_NAME_INPUT_HINT_TEXT = config["register_screen_settings"]["user_name_input_hint_text"]
REGISTER_SCREEN_SUBMIT_BUTTON_TEXT = config["register_screen_settings"]["submit_button_text"]
MAIN_MENU_SCREEN_MAIN_MENU_LABEL_TEXT = config["main_menu_screen_settings"]["main_menu_label_text"]
MAIN_MENU_SCREEN_SHOW_DICTIONARY_BUTTON_TEXT = config["main_menu_screen_settings"]["show_dictionary_button_text"]
MAIN_MENU_SCREEN_SHOW_TRAINING_BUTTON_TEXT = config["main_menu_screen_settings"]["show_training_button_text"]
