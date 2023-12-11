import sqlite3
import traceback

from helpers.const import UserData, SocCred
from helpers.helpers import get_unreadable_social_credits, get_readable_social_credits


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
        request: str = f"SELECT UserID FROM Users WHERE UserID={user_id}"
        
        try: 
            responce = self.execute_request(request, True)
            return bool(len(responce))
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
          
    def add_user(self, user_id: int, special_signs: str, social_credits: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request: str = "INSERT INTO Users ( UserID, SpecialSigns, SocialPoints, IsInfinity, PhotoCards ) VALUES " \
                       f"( {user_id}, \"{special_signs}\", {social_credits}, {is_infinity}, \"{photo_cards}\" )"
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False
    
    def edit_user(self, user_id: int, special_signs: str, social_credits: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request = "UPDATE Users " \
                  f"SET SpecialSigns = \"{special_signs}\", SocialPoints = {social_credits}, " \
                  f"IsInfinity = {is_infinity}, PhotoCards = \"{photo_cards}\" " \
                  f"WHERE UserID = {user_id}"
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return False

    def get_user_data(self, user_id: int, name: str) -> UserData:
        request: str = f"SELECT * FROM Users WHERE UserID={user_id}"
        try: 
            responce = self.execute_request(request, True)
            return UserData(name, responce[0][1], responce[0][2], 
                            responce[0][3], responce[0][4].split())
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)

    def update_rep(self, user_id: int, rep: str) -> str:
        # TODO: if rating == "+-inf", return submit message 
        if not self.user_exists(user_id):
            return "Сначала добавьте пользователя"
        social_credits, is_infinity = get_unreadable_social_credits(rep)
        insertion = social_credits
        if is_infinity == SocCred.GET_FROM_DB:
            request: str = f"SELECT SocialPoints FROM Users WHERE UserID={user_id}"
            insertion += int(self.execute_request(request, True)[0][0])
            
        request: str = "UPDATE Users SET " \
                       f"SocialPoints = {insertion}, IsInfinity = {is_infinity} " \
                       f"WHERE UserID={user_id}"
        self.execute_request(request, False)
        data: UserData = self.get_user_data(user_id, "")
        curr_rate = get_readable_social_credits(data.social_credits, data.is_infinity)
        return f"Текущий рейтинг пользователя: {curr_rate}"