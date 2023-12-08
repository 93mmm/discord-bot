from random import randint

class Bot:
    DB_PATH: str = "files/database/database.db"
    TOKEN: str = "token"
    GUILD_ID: int = 0 # Right click on the server image and click copy id
    ADMINISTRATORS: list[int] = [0]


class SocCred:
    GET_FROM_DB: int = 0
    P_INFINITY: int = 1
    N_INFINITY: int = 2


class Assets:
    ASSETS: dict[str, str] = dict()
    ASSETS["амёба"] = "files/assets/Амёба_ебаная.png"
    ASSETS["анархист"] = "files/assets/Анархист.png"
    ASSETS["анимешник"] = "files/assets/Анимешник.png"
    ASSETS["верун"] = "files/assets/Верун.png"
    ASSETS["виндузятник"] = "files/assets/Виндузятник.png"
    ASSETS["вкатун"] = "files/assets/Вкатуноид.png"
    ASSETS["герой-сервера"] = "files/assets/Герою_сервера.png"
    ASSETS["жид"] = "files/assets/Жыд.png"
    ASSETS["занятой"] = "files/assets/Занятой.png"
    ASSETS["засвободец"] = "files/assets/Засвободец.png"
    ASSETS["зумер"] = "files/assets/Зумер.png"
    ASSETS["исламист"] = "files/assets/Исламист.png"
    ASSETS["киберспортсмен"] = "files/assets/Киберспортсмен.png"
    ASSETS["коммунист"] = "files/assets/Коммуняка.png"
    ASSETS["лгбт"] = "files/assets/ЛГБТ_СЖВ.png"
    ASSETS["маковец"] = "files/assets/Маковец.png"
    ASSETS["тролль"] = "files/assets/Мамкин_тролепан.png"
    ASSETS["меломан"] = "files/assets/Меломан_говноед.png"
    ASSETS["работяга"] = "files/assets/Работяга.png"
    ASSETS["рядовой"] = "files/assets/Рядовой.png"
    ASSETS["фашист"] = "files/assets/Фошизд.png"

    ASSETS["python"] = "files/assets/Питонист.png"
    ASSETS["c++"] = "files/assets/Плюсовик.png"
    ASSETS["rust"] = "files/assets/Растер.png"
    ASSETS["js"] = "files/assets/Яваскриптизёр.png"
    ASSETS["linux"] = "files/assets/Линуксоид.png"

    PRINT: str = "files/assets/Печать.png"
    CARD: str = "files/assets/Карточка_социального_рейтинга.png"


class Fonts:
    HEADINGS: str = "files/fonts/tahyp.ttf"
    PLAIN: str = "files/fonts/ttwp.ttf"


class Positions:
    NAME: tuple[int, int] = (130, 63)
    PHOTO_CARDS: list[tuple[int, int]] = [
        (210, 115),
        (330, 115),
        (450, 115)
        ]
    SPECIAL_SIGNS: list[tuple[int, int]] = [
        (300, 224),
        (50, 253),
        (50, 283),
        ]
    FIRST_ROW_LEN: int = 300
    NEXT_ROW_LEN: int = 540
    
    PRINT_SIZE: tuple[int, int] = (256, 256)
    
    def PRINT_POS() -> tuple[int, int]:
        PRINT_X = 550
        PRINT_Y = 60
        return (PRINT_X + randint(0, 40), PRINT_Y + randint(0, 40))
    
    def PRINT_ANGLE() -> int:
        return -15 + randint(-5, 10)
    

class UserData:
    def __init__(self, name: str, special_signs: str, social_points: str, 
                 is_infinity: str, photo_cards: list[str]) -> None:
        self.name: str = name
        self.special_signs: str = special_signs
        self.social_points: str = social_points
        self.is_infinity: str = is_infinity
        self.photo_cards: list[str] = photo_cards
    
    def get_paths(self) -> list[str]:
        for i in range(len(self.photo_cards)):
            self.photo_cards[i] = Assets.ASSETS[self.photo_cards[i].lower()]
        return self.photo_cards


# TODO: +inf -inf только при заведении  карточки
