class Consts:
    PATH: str = "files/database/database.db"
    TABLE_NAME: str = "Users"
    USER_ID: str = "UserID"
    SPECIAL_SIGNS: str = "SpecialSigns"
    SOCIAL_POINTS: str = "SocialPoints"
    IS_INFINITY: str = "IsInfinity"
    PHOTO_CARDS: str = "PhotoCards"

class Bot:
    TOKEN: str = "MTE3Njk0ODI3NjUwNzk4Mzk0Mw.G3rsZV.kmyNVqTyCu0RM-ECeIXwRqFhgf1Zs35B_v0M4E"
    GUILD_ID: int = 1176988728275775498 # Right click on the server image and click copy id
    ADMINISTRATORS: list[int] = [0]

class SocCred:
    GET_FROM_DB: int = 0
    PL_INFINITY: int = 1
    MIN_INFINITY: int = 2

class UserData:
    def __init__(self, special_signs: str, social_points: str, 
                 is_infinity: str, photo_cards: list[str]) -> None:
        self.special_signs = special_signs
        self.social_points = social_points
        self.is_infinity = is_infinity
        self.photo_cards = photo_cards

      
