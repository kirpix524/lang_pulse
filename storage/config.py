import json

CONFIG_PATH = "settings.json"
with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

USERS_DB_FILE = config["users_db_file"]
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
