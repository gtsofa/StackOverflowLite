from config import conn

class User:
    """
    Implement a user
    """
    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    @staticmethod
    def create_user(cursor, username, email, password, confirm_password):
        query = "INSERT INTO users (username, email, password, confirm_password) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (username, email, password, confirm_password))
        conn.commit()

    @staticmethod
    def get_users(cursor):
        query = "SELECT * FROM users;"
        cursor.execute(query)
        users = cursor.fetchall()
        results = []
        for user in users:
            details = {}
            details["user_id"] = user[0]
            details["username"] = user[1]
            details["email"] = user[2]
            details["password"] = user[3]
            details["confirm_password"] = user[4]
            results.append(details)

        return results

    # @staticmethod
    # def login(cursor, username, password):
    #     query = "INSERT INTO users(username, password) VALUES(%s, %s);"
    #     cursor.execute(query, (username, password))
    #     conn.commit()
