from helpers.const import SocCred

def get_unreadable_social_credits(info: str) -> tuple[int, int]:
    # ! receives string (possible cases: +inf, -inf, +number, -number)
    # ! returns information that can be fitted into database 
    # ! (social credits: number, is_infinity (rating usage determinator))
    social_credits = 0
    is_infinity = SocCred.GET_FROM_DB
    if info.startswith("+inf"):
        is_infinity = SocCred.P_INFINITY
    elif info.startswith("-inf"):
        is_infinity = SocCred.N_INFINITY
    else:
        social_credits = int(info)
    return social_credits, is_infinity

def get_readable_social_credits(social_credits: str, is_infinity: str):
    if is_infinity == SocCred.N_INFINITY:
        return "-inf"
    elif is_infinity == SocCred.P_INFINITY:
        return "+inf"
    return social_credits

def iter_arrs(*args):
    for i in range(min(map(len, args))):
        out = list()
        for a in args:
            out.append(a[i])
        yield out