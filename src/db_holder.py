import sqlite3
from src.const import Consts, UserData, SocCred


def get_soc_rating_for_db(info: str):
    social_points = 0
    is_infinity = SocCred.GET_FROM_DB
    if info.startswith("+inf"):
        is_infinity = SocCred.P_INFINITY
    elif info.startswith("-inf"):
        is_infinity = SocCred.N_INFINITY
    else:
        social_points = int(info)
    return social_points, is_infinity


def soc_rating_in_form(is_infinity: str, points: str):
    if is_infinity == SocCred.N_INFINITY:
        return "-inf"
    elif is_infinity == SocCred.P_INFINITY:
        return "+inf"
    return points
    

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
        request: str = f"""SELECT {Consts.USER_ID} FROM 
                           {Consts.TABLE_NAME}
                           WHERE {Consts.USER_ID}={user_id}"""
        
        try: 
            responce = self.execute_request(request, True)
            return bool(len(responce))
        except sqlite3.IntegrityError as ex:
            print(ex)
          
    def add_user(self, user_id: int, special_signs: str, social_points: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request: str = f"""INSERT INTO {Consts.TABLE_NAME} 
                           ( {Consts.USER_ID}, {Consts.SPECIAL_SIGNS}, {Consts.SOCIAL_POINTS}, {Consts.IS_INFINITY}, {Consts.PHOTO_CARDS} )
                           VALUES
                           ( {user_id}, \"{special_signs}\", {social_points}, {is_infinity}, \"{photo_cards}\" )"""
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            print(ex)
            return False
    
    def edit_user(self, user_id: int, special_signs: str, social_points: str,
                 is_infinity: str, photo_cards: str) -> bool:
        request = f"""UPDATE {Consts.TABLE_NAME} 
                     SET {Consts.SPECIAL_SIGNS} = \"{special_signs}\", {Consts.SOCIAL_POINTS} = {social_points}, 
                     {Consts.IS_INFINITY} = {is_infinity}, {Consts.PHOTO_CARDS} = \"{photo_cards}\" 
                     WHERE UserID = {user_id}"""
        try: 
            self.execute_request(request)
            return True
        except sqlite3.IntegrityError as ex:
            print(ex)
            return False
    
    def update_rep(self, user_id: int, rep: str) -> bool:
        pass
        
    def get_data(self, user_id: int) -> UserData:
        request: str = f"""SELECT * FROM 
                           {Consts.TABLE_NAME}
                           WHERE {Consts.USER_ID}={user_id}"""
        try: 
            responce = self.execute_request(request, True)
            return UserData(responce[0][1], responce[0][2], 
                            responce[0][3], responce[0][4].split())
        except sqlite3.IntegrityError as ex:
            print(ex)
