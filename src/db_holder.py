import sqlite3
from src.const import Consts, UserData

class Database:
    def __init__(self, filename: str):
        self.connection: sqlite3.Connection = sqlite3.connect(filename)
    
    def __del__(self):
        self.connection.close()
    
    def execute_request(self, request: str, awaiting_data: bool=False) -> list[tuple[str]]:
        cur: sqlite3.Cursor = self.connection.cursor()

        responce = cur.execute(request).fetchall()
        print(responce, awaiting_data)
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
        request = """UPDATE """
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