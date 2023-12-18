from constants import PATHS, KEY_CONFIG
import os


def path_config_check() -> bool:
    badges: dict[str, str] = PATHS["badges"]
    out: bool = True
    for key, value in badges.items():
        if not os.path.exists(value):
            out = False
            print(f"file {value} with key {key} in CONFIG does not exists!")
    return out


def key_config_check() -> bool:
    badges_keys: dict[str, list[str]] = KEY_CONFIG["badges"]
    badges_paths: dict[str, str] = PATHS["badges"]
    out: bool = True

    for key, val in badges_keys.items():
        if key not in badges_paths:
            out = False
            print(f"key {key} does not exists in path-config.json")

    return out


def tests() -> None:
    path_config_check()
    key_config_check()


if __name__ == "__main__":
    tests()
