from src.helpers.const import SocCred


def get_soc_rating_for_db(info: str) -> tuple[int, int]:
    # ! receives string (possible cases: +inf, -inf, +number, -number)
    # ! returns information that can be fitted into database 
    # ! (social points: number, is_infinity (rating usage determinator))
    social_points = 0
    is_infinity = SocCred.GET_FROM_DB
    if info.startswith("+inf"):
        is_infinity = SocCred.P_INFINITY
    elif info.startswith("-inf"):
        is_infinity = SocCred.N_INFINITY
    else:
        social_points = int(info)
    return social_points, is_infinity


def soc_rating_in_form(social_points: str, is_infinity: str):
    if is_infinity == SocCred.N_INFINITY:
        return "-inf"
    elif is_infinity == SocCred.P_INFINITY:
        return "+inf"
    return social_points
