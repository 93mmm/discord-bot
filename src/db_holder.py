import sqlite3
from src.const import Consts

class Database:
    def __init__(self, filename: str):
        self.connection: sqlite3.Connection = sqlite3.connect(filename)
      
    def user_exists(self, id: int) -> bool:
        cur: sqlite3.Cursor = self.connection.cursor()
        request: str = f"""SELECT * FROM 
                           {Consts.TABLE_NAME}
                           WHERE {Consts.USER_ID}={id}"""
        try: 
            responce = cur.execute(request).fetchall()
            if len(responce):
                return True
            return False
        except sqlite3.IntegrityError as ex:
            print(ex)
          

    def add_user(self, id: int, username: str, spec_signs: str, soc_points: int) -> None:
        self.user_exists(id)
        cur: sqlite3.Cursor = self.connection.cursor()
        if self.user_exists(id):
            to_update: list[str] = [f"{Consts.USERNAME} = \"{username}\""]
            print(spec_signs)
            if spec_signs != "":
                to_update.append(f"{Consts.SPECIAL_SIGNS} = \"{spec_signs}\"")
            if soc_points != 0:
                to_update.append(f"{Consts.SOCIAL_POINTS} = {soc_points}")
            
            request: str = f"""UPDATE 
                               {Consts.TABLE_NAME}
                               SET {', '.join(to_update)}
                               WHERE {Consts.USER_ID} = {id}
"""
            print(request)
        else:
            request: str = f"""INSERT INTO 
                              {Consts.TABLE_NAME} 
                              ({Consts.USER_ID}, {Consts.USERNAME}, {Consts.SPECIAL_SIGNS}, {Consts.SOCIAL_POINTS}) 
                              VALUES 
                              ({id}, \"{username}\", \"{spec_signs}\", \"{soc_points}\")"""

        
        try: 
            cur.execute(request)
            self.connection.commit()
        except sqlite3.IntegrityError as ex:
            print(ex)