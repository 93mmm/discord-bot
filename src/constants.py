from config import get_config, get_paths


class SocCred:
    GET_FROM_DB: int = 0
    P_INFINITY: int = 1
    N_INFINITY: int = 2


PATHS: dict = get_paths()
CONFIG: dict = get_config()
