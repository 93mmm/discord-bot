import sqlite3
import traceback

from helpers import User


class Database:
    def __init__(self, filename: str):
        self.connection: sqlite3.Connection = sqlite3.connect(filename)

    def __del__(self):
        self.connection.close()

    def execute_request(self, request: str,
                        awaiting_data: bool = False) -> list[tuple[str]]:
        cur: sqlite3.Cursor = self.connection.cursor()

        try:
            responce = cur.execute(request).fetchall()
            if awaiting_data:
                return responce
            self.connection.commit()
        except sqlite3.IntegrityError as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)

    def get_user(self, user_id: int) -> User:
        if not self.user_exists(user_id):
            data: User = User(user_id)
        else:
            request: str = f"SELECT * FROM Users WHERE UserID={user_id}"
            responce = self.execute_request(request, True)[0]
            data: User = User(user_id,
                              responce[1],
                              responce[2],
                              responce[3],
                              responce[4])
        return data

    def add_user(self, usr: User) -> None:
        request: str = "INSERT INTO Users ( UserID, SpecialSigns, " \
                "SocialCredits, IsInfinity, Badges) VALUES " \
                f"( {usr.user_id}, \"{usr.special_signs}\", " \
                f"{usr.social_credits}, {usr.is_infinity}, " \
                f"\"{usr.badges}\" )"
        self.execute_request(request)

    def update_user(self, usr: User) -> None:
        request: str = "UPDATE Users SET " \
                f"SpecialSigns = \"{usr.special_signs}\", " \
                f"Badges = \"{usr.badges}\" " \
                f"WHERE UserID = {usr.user_id}"
        self.execute_request(request)

    def update_rep(self, user_id: int, rep: int) -> None:
        rep += self.get_social_credits(user_id)[0]
        request: str = "UPDATE Users SET " \
                       f"SocialCredits = {rep} WHERE UserID={user_id}"
        self.execute_request(request, False)

    def user_exists(self, user_id: int) -> bool:
        request: str = f"SELECT UserID FROM Users WHERE UserID={user_id}"
        responce = self.execute_request(request, True)
        return bool(len(responce))

    def get_social_credits(self, user_id: int) -> int:
        usr: User = self.get_user(user_id)
        return (usr.social_credits, usr.is_infinity)
