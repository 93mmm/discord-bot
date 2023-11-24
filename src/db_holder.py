import sqlite3
from src.const import Consts, UserData

class Database:
    def __init__(self, filename: str):
        self.connection: sqlite3.Connection = sqlite3.connect(filename)
    
    def __del__(self):
        self.connection.close()
      
    def user_exists(self, user_id: int) -> bool:
        cur: sqlite3.Cursor = self.connection.cursor()
        request: str = f"""SELECT * FROM 
                           {Consts.TABLE_NAME}
                           WHERE {Consts.USER_ID}={user_id}"""
        try: 
            responce = cur.execute(request).fetchall()
            if len(responce):
                return True
            return False
        except sqlite3.IntegrityError as ex:
            print(ex)
          

    def add_user(self, user_id: int, special_signs: str, social_points: str,
                 is_infinity: str, photo_cards: str) -> str:
        cur: sqlite3.Cursor = self.connection.cursor()

        request: str = f"""INSERT INTO {Consts.TABLE_NAME} 
                           ( {Consts.USER_ID}, {Consts.SPECIAL_SIGNS}, {Consts.SOCIAL_POINTS}, {Consts.IS_INFINITY}, {Consts.PHOTO_CARDS} )
                           VALUES
                           ( {user_id}, \"{special_signs}\", {social_points}, {is_infinity}, \"{photo_cards}\" )"""
        try: 
            cur.execute(request)
            self.connection.commit()
            return "User successfully added into database"
        except sqlite3.IntegrityError as ex:
            print(ex)
            return "Exception"
    
    def update_rep(self, user_id: int, rep: str):
        pass
        
    def get_data(self, user_id: int) -> UserData:
        cur: sqlite3.Cursor = self.connection.cursor()
        request: str = f"""SELECT * FROM 
                           {Consts.TABLE_NAME}
                           WHERE {Consts.USER_ID}={user_id}"""
        try: 
            responce = cur.execute(request).fetchall()
            print(responce)
            return UserData(responce[0][1], responce[0][2], 
                            responce[0][3], responce[0][4].split())
        except sqlite3.IntegrityError as ex:
            print(ex)