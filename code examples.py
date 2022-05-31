class superhero():
    def __init__(self):
        # Initialise Datastore
        """
        Initialise Datastore
        """

        self.filename = "superhero.db"
        # Checks to see if database exists, if it does it will connect. If it doesn't it will create the database and import the csv values
        if not os.path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()
            self.create_superhero_database()
            self.import_csv()
        else:
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()

    def create_superhero_database(self):
        # Uses SQL code to create the database
        """
        Creates the data structure for the superhero database
        """

        self.cursor.execute("""
                            CREATE TABLE Superhero(
                                super_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                super_name TEXT NOT NULL,
                                super_intelli INTEGER,
                                super_stren INTEGER,
                                super_spd INTEGER,
                                super_dur INTEGER,
                                super_pow INTEGER,
                                super_comb INTEGER,
                                super_image TEXT NOT NULL
                            )
                            """)

        self.cursor.execute("""
                            CREATE TABLE Alias(
                                alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                super_id INTEGER,
                                alias_name TEXT NOT NULL,
                                FOREIGN KEY(super_id) REFERENCES Superhero(super_id)                                
                            )
                            """)
        
        self.cursor.execute("""
                            CREATE TABLE Users(
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_email TEXT NOT NULL,
                                user_pass TEXT NOT NULL,
                                user_wins INTEGER,
                                user_loss INTEGER
                            )
                            """)

# -------

# FILE 1

def user_login(self, username, password):
    # Checks values are in database, if they are then it changes the logged in status to logged in.
        """
        lets users login to their accounts
        
        username: str
        password: str
        """
        # Checks if the user is in the database
        self.cursor.execute(
            """
            SELECT user_name 
            FROM user
            """
            )
        results_name = self.cursor.fetchall()
        for record in results_name:
            if str(record[0]) == username:
                # Checks if the password is correct
                self.cursor.execute(
                    """
                    SELECT user_password 
                    FROM user
                    WHERE user_name = :username
                    """,
                    {
                        "username": username
                    }
                )
                result_password = self.cursor.fetchall()[0][0]
                # if password does exist in the database then it will change log in value to true and it will print the username
                if result_password == password:
                    self.login = True
                    print(self.login)
                    self.username = username
                    return("logged in")
                else:
                    self.login = False
            
        if self.login == True:
            return self.login
        else:
            self.login = False
            return self.login

# FILE 2

    def loginuser(self):
        # Gathers user inputs from lineEdit widgets
        recentUsername = self.username_input.text()
        recentPassword = self.password_input.text()
        print()
        # Passes user inputs as variables to be checked in the database
        UserDB.user_login(self, username= recentUsername, password = recentPassword)
        print(recentUsername)
        print(recentPassword)

# ------

# FILE 1
# Creating functions that change the difficulty and decksize value based on button presses or user text inputs
    def diffeasy(self):
        self.difficulty = "easy"
        
    def diffmed(self):
        self.difficulty = "med"

    def diffhard(self):
        self.difficulty = "hard"
    
    def getdiff(self):
        return self.difficulty

    def decksize(self):
        self.pack_size = int(self.lineEdit.text())

    def getdecksize(self):
        return self.pack_size

# FILE 2
# Setting game difficulty and deck size to whatever the user has picked
    self.difficulty = difficulty
    print("the difficulty is set to: ", difficulty)

    self.pack_size = pack_size
    print("the player deck is set to: ", pack_size)

# ----------

    def compare_stat(self, player_stat, ai_stat):
        # Compares the chosen player stat to the randomly chosen Ai stat.
        print(player_stat,ai_stat)
        if player_stat > ai_stat:
            return "player"
        elif player_stat < ai_stat:
            return "ai"
        else:
            return "draw"

# ----------
# Opens the game window and closes the main menu window
# this function also passes through the difficulty and pack_size arguments to the game.py file
    def rungamewin(self):
        if hasattr(self, 'ui'):
            self.difficulty = self.ui.getdiff()
            self.pack_size = self.ui.getdecksize()
        main_window = GameScreen.MainWindow(self.difficulty, self.pack_size)
        main_window.show()
        MainWindow.close()