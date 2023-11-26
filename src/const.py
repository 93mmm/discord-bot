class Consts:
    PATH: str = "files/database/database.db"
    TABLE_NAME: str = "Users"
    USER_ID: str = "UserID"
    SPECIAL_SIGNS: str = "SpecialSigns"
    SOCIAL_POINTS: str = "SocialPoints"
    IS_INFINITY: str = "IsInfinity"
    PHOTO_CARDS: str = "PhotoCards"


class Bot:
    TOKEN: str = "token"
    GUILD_ID: int = 0 # Right click on the server image and click copy id
    ADMINISTRATORS: list[int] = [0]


class SocCred:
    GET_FROM_DB: int = 0
    P_INFINITY: int = 1
    N_INFINITY: int = 2


class UserData:
    def __init__(self, special_signs: str, social_points: str, 
                 is_infinity: str, photo_cards: list[str]) -> None:
        self.special_signs: str = special_signs
        self.social_points: str = social_points
        self.is_infinity: str = is_infinity
        self.photo_cards: list[str] = photo_cards

