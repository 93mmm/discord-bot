import discord as ds
from uuid import uuid4
from os import remove
from random import randint

from constants import SocCred, CONFIG, PATHS


class User:
    def __init__(self,
                 user_id: int,
                 special_signs: str="",
                 social_credits: int=0,
                 is_infinity: int=0,
                 badges: str="") -> None:

        assert(type(user_id) == int)
        assert(type(special_signs) == str)
        assert(type(social_credits) == int)
        assert(type(is_infinity) == int)
        assert(type(badges) == str)

        self.user_id: int = user_id
        self.special_signs: str = special_signs
        self.social_credits: str = social_credits
        self.is_infinity: str = is_infinity
        self.badges: str = badges

    def get_paths(self) -> list[str]:
        out: list[str] = list()
        badges_array: list[str] = self.badges.split(" ")
        for i in range(len(badges_array)):
            out.append(PATHS["badges"][badges_array[i].lower()])
        return out


class TmpImg:
    def __init__(self) -> None:
        self._fn = f"files/tmp/{uuid4()}.png"

    def close(self) -> None:
        remove(self._fn)

    def filename(self) -> str:
        return self._fn


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


def get_errmsg_rep(user_id: int,
                   member: ds.Member,
                   social_credits: str,
                   db):
    if user_id not in CONFIG["administrators"]:
        return "Вы не админ"

    if member is None:
        return "Пользователь не указан"

    if social_credits == "":
        return "Социальный рейтинг не указан"

    if social_credits.startswith("+inf") or social_credits.startswith("-inf"):
        return "Нельзя указать бесконечный рейтинг"

    if not db.user_exists(member.id):
        return "Сначала добавьте пользователя"

    if db.get_social_credits(member.id)[1] != SocCred.GET_FROM_DB:
        return "У пользователя бесконечный рейтинг"

    return ""


def iter_arrs(*args):
    for i in range(min(map(len, args))):
        out = list()
        for a in args:
            out.append(a[i])
        yield out


def print_position() -> tuple[int, int]:
    x: int = 550 + randint(0, 40)
    y: int = 60 + randint(0, 40)
    return (x, y)


def print_angle() -> int:
    return -15 + randint(-5, 10)
