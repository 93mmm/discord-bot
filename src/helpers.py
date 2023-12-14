from constants import SocCred


class User:
    def __init__(self,
                 user_id: int,
                 special_signs: str="",
                 social_credits: int=0,
                 is_infinity: int=0,
                 badges: str="") -> None:

        assert(type(user_id) == int and
               type(special_signs) == str and
               type(social_credits) == int and
               type(is_infinity) == int and
               type(badges) == str)

        self.user_id: int = user_id
        self.special_signs: str = special_signs
        self.social_credits: str = social_credits
        self.is_infinity: str = is_infinity
        self.badges: str = badges

    def get_paths(self):
        pass


def credits_for_db(rating: str) -> tuple[int, int]:
    # ! receives string (possible cases: +inf, -inf, +number, -number)
    social_credits = 0
    is_infinity = SocCred.GET_FROM_DB

    # ! (social points: number, is_infinity (rating usage determinator))
    if rating.startswith("+inf"):
        is_infinity = SocCred.P_INFINITY
    elif rating.startswith("-inf"):
        is_infinity = SocCred.N_INFINITY
    else:
        social_credits = int(rating)

    # ! returns information that can be fitted into database
    return social_credits, is_infinity


def credits_for_form(social_points: str, is_infinity: str):
    if is_infinity == SocCred.N_INFINITY:
        return "-inf"
    elif is_infinity == SocCred.P_INFINITY:
        return "+inf"

    return social_points
