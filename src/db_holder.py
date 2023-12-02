import sqlite3
import traceback

from src.const import UserData, SocCred


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
    

class Database:
    def __init__(self, filename: str):
        self.connection: sqlite3.Connection = sqlite3.connect(filename)
    
    def __del__(self):
        self.connection.close()
    
    def execute_request(self, request: str, awaiting_data: bool=False) -> list[tuple[str]]:
        cur: sqlite3.Cursor = self.connection.cursor()

        responce = cur.execute(request).fetchall()
        if awaiting_data:
            return responce
        self.connection.commit()
      
    def user_exists(self, user_id: int) -> bool:
        request: str = f"""SELECT UserID FROM Users WHERE UserID={user_id}"""
        
        try: 
            responce = self.execute_request(request, True)
            return bool(len(responce))
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
          
    def add_user(self, user_id: int, special_signs: str, social_points: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request: str = f"""INSERT INTO Users
                           ( UserID, SpecialSigns, SocialPoints, IsInfinity, PhotoCards )
                           VALUES
                           ( {user_id}, \"{special_signs}\", {social_points}, {is_infinity}, \"{photo_cards}\" )"""
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False
    
    def edit_user(self, user_id: int, special_signs: str, social_points: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request = f"""UPDATE Users
                     SET SpecialSigns = \"{special_signs}\", SocialPoints = {social_points}, 
                     IsInfinity = {is_infinity}, PhotoCards = \"{photo_cards}\" 
                     WHERE UserID = {user_id}"""
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False

    def get_user_data(self, user_id: int) -> UserData:
        request: str = f"""SELECT * FROM Users
                           WHERE UserID={user_id}"""
        try: 
            responce = self.execute_request(request, True)
            return UserData(responce[0][1], responce[0][2], 
                            responce[0][3], responce[0][4].split())
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)

    def update_rep(self, user_id: int, rep: str) -> str:
        # TODO: if rating == "+-inf", return submit message 
        if not self.user_exists(user_id):
            return "Сначала добавьте пользователя"
        social_points, is_infinity = get_soc_rating_for_db(rep)
        insertion = social_points
        if is_infinity == SocCred.GET_FROM_DB:
            request: str = f"""SELECT SocialPoints FROM Users
                           WHERE UserID={user_id}"""
            insertion += int(self.execute_request(request, True)[0][0])
            
        request: str = f"""UPDATE Users SET 
                           SocialPoints = {insertion}, IsInfinity = {is_infinity}
                           WHERE UserID={user_id}"""
        self.execute_request(request, False)
        data: UserData = self.get_user_data(user_id)
        curr_rate = soc_rating_in_form(data.social_points, data.is_infinity)
        return f"Текущий рейтинг пользователя: {curr_rate}"
