from config import get_config, get_paths, get_key_config


class SocCred:
    GET_FROM_DB: int = 0
    P_INFINITY: int = 1
    N_INFINITY: int = 2


class Positions:
    USERNAME: tuple[int, int] = (130, 63)

    SPECIAL_SIGNS: list[tuple[int, int]] = [
            (300, 224),
            (50, 253),
            (50, 283),
            ]

    ROWS: list[int] = [
            300,
            540
            ]

    SOCIAL_CREDITS: tuple[int, int] = (375, 330)

    BADGES: list[tuple[int, int]] = [
        (195, 115),
        (295, 115),
        (395, 115),
        (495, 115)
        ]

    PRINT_SIZE: tuple[int, int] = (256, 256)


PATHS: dict = get_paths()
CONFIG: dict = get_config()
KEY_CONFIG: dict = get_key_config()
