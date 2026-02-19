from pathlib import Path
from platformdirs import (
    user_config_dir,
    user_data_dir,
    user_cache_dir,
    user_log_dir,
    user_documents_dir,
    user_downloads_dir,
    user_desktop_dir,
    user_pictures_dir,
    user_videos_dir,
    user_music_dir
)

APP_NAME = "genban"
APP_AUTHOR = "DIY"

def get_path(path_str) -> Path:
    p = Path(path_str)
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_config_dir() -> Path:
    return get_path(user_config_dir(APP_NAME, APP_AUTHOR))

def get_data_dir() -> Path:
    return get_path(user_data_dir(APP_NAME, APP_AUTHOR))

def get_cache_dir() -> Path:
    return get_path(user_cache_dir(APP_NAME, APP_AUTHOR))

def get_log_dir() -> Path:
    return get_path(user_log_dir(APP_NAME, APP_AUTHOR))

def get_app_dirs() -> list:
    return [
        user_config_dir(APP_NAME, APP_AUTHOR),
        user_data_dir(APP_NAME, APP_AUTHOR),
        user_cache_dir(APP_NAME, APP_AUTHOR),
        user_log_dir(APP_NAME, APP_AUTHOR)
    ]

def get_user_dirs() -> list:
    return [
        user_documents_dir(),
        user_downloads_dir(),
        user_desktop_dir(),
        user_pictures_dir(),
        user_videos_dir(),
        user_music_dir()
    ]

def validate_path(path, whitelist: list) -> bool:
    return any(path.startswith(whitelist_item) for whitelist_item in whitelist)