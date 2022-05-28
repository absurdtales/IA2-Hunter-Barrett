import sqlite3
import os
import csv
import requests
import shutil

class UserDB():
    def __init__(self):
        self.file = "Users.db"

        if not os.path.exists(self.file):
            # if db is not present create it then connect to it
            self.conn = sqlite3.connect(self.file)
            self.cursor = self.conn.cursor()
            self.create_user_db()
            self.login = False
            self.username = ""
        else:
            self.conn = sqlite3.connect(self.file)
            self.cursor = self.conn.cursor()
            self.login = False
            self.username = ""
    
    def create_user_db(self):
        """
        Creates the data structure for the superhero database
        """

        # create users table
        self.cursor.execute("""
                            CREATE TABLE Users(
                                user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_email TEXT NOT NULL,
                                user_name TEXT NOT NULL,
                                user_password TEXT NOT NULL,
                                user_wins INTEGER,
                                user_loss INTEGER
                            )
                            """)

    def create_user(self, username, email, password):
        """
        Add new member details
        
        username: str
        email: str
        password: str
        """
        #check if email is used
        self.cursor.execute(
            """
            SELECT user_email 
            FROM Users
            """
            )
        results_email = self.cursor.fetchall()
        for record in results_email:
            if record[0] == email:
                #check if username is used
                self.cursor.execute(
                    """
                    SELECT user_name 
                    FROM Users
                    """
                    )
                results_name = self.cursor.fetchall()
                for record in results_name:
                    if record[0] == username:
                       return("email and username already used")
                    else:
                        return("email already used")

            else: 
                #check if username is used
                self.cursor.execute(
                    """
                    SELECT user_name 
                    FROM Users
                    """
                    )
                results_name = self.cursor.fetchall()
                for record in results_name:
                    if record[0] == username:
                       return("username already used")
                       #find highest member id
                
                    else:
                        self.cursor.execute(
                           """
                           SELECT MAX(user_ID)
                           FROM Users
                           """
                           )
                        user_ID = self.cursor.fetchone()[0] + 1
                        # add details to database
                        self.cursor.execute(
                           """
                           INSERT INTO Users
                           VALUES (:ID, :name, :email, :password)
                           """,
                           {
                               "ID": user_ID, 
                               "name": username,
                               "email": email,
                               "password": password
                           }
                        )
                        self.conn.commit()
                        return("account created")

    def user_login(self, username, password):
        """
        lets users login to their accounts
        
        username: str
        password: str
        """
        # check if user is in databse
        self.cursor.execute(
            """
            SELECT user_name 
            FROM Users
            """
            )
        results_name = self.cursor.fetchall()
        for record in results_name:
            if record[0] == username:
                #continues to check if the password is correct
                self.cursor.execute(
                    """
                    SELECT user_password 
                    FROM Users
                    WHERE user_name = :username
                    """,
                    {
                        "username": username
                    }
                )
                result_password = self.cursor.fetchall()[0]
                
                if result_password == password:
                    self.login = True
                    self.username = username
                    return("logged in")
                else:
                    return("incorrect password, please try agian")
            else:
                return("username not found, please create an account then try logging in")

    def check_stats(self):
        user_match = 0
        results_modified = []
        if self.username == "":
            return("please login to view stats")
        else:
            self.cursor.execute(
                """
                SELECT match_ID, win_loss, ai_dif 
                FROM winloss
                WHERE user_ID 
                IN (SELECT user_ID 
                    FROM Users 
                    WHERE user_name = :username)
                """,
                {
                    "username": self.username 
                }
            )
            results = self.cursor.fetchall()
            for record in results:
                user_match = user_match + 1
                match_result = record[1]
                match_dif = record [2]
                match_tuple = (user_match, match_result, match_dif)
                results_modified.append(match_tuple)

            return(results_modified)
    
    def add_stat(self, ai_dif, match_result):
        """
        adds the result of a match to the winloss table

        ai_dif: str
        match_result: str
        """
        self.cursor.execute(
            """
            SELECT user_ID
            FROM Users
            WHERE user_name = :username
            """,
            {
                "username": self.username
            }
        )
UserDB.create_user('yeah', 'bruh', 'yeah', 'uhuh')