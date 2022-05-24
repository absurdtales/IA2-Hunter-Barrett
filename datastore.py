import sqlite3
import os
import csv
import requests
import shutil

class superhero():
    def __init__(self):
        """
        Initialise Datastore
        """

        self.filename = "superhero.db"
        
        if not os.path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()
            self.create_superhero_database()
            self.import_csv()
        else:
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()

    def create_superhero_database(self):
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

    def import_csv(self):
        """
        Load values from csv into database
        """

        with open("superhero.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for index, superhero in enumerate(csv_reader):
                # read the values for a single hero 
                if index > 0:
                    name = superhero[0]
                    intelligence = self.clean_nulls(superhero[1])
                    strength = self.clean_nulls(superhero[2])
                    speed = self.clean_nulls(superhero[3])
                    durability = self.clean_nulls(superhero[4])
                    power = self.clean_nulls(superhero[5])
                    combat = self.clean_nulls(superhero[6])
                    aliases = superhero[9]
                    image = superhero[26]

                    # get image
                    image_path = self.get_image(image)

                    # add superhero to Superhero table
                    self.add_superhero((name,
                                        intelligence,
                                        strength,
                                        speed,
                                        durability,
                                        power,
                                        combat,
                                        image_path,
                                        ))

                    # process aliases
                    if aliases != "-":
                        superh_id = self.get_last_superhero_id()
                        for alias in self.get_alias_list(aliases):
                            self.add_alias((alias,superh_id))

                    
                print(f"{index+1} records processed")

    def clean_nulls(self,val):
        """
        Check if a superhero value is null
        """
        if val == "null":
            return None
        else:
            return int(val)

    def get_alias_list(self,aliases):
            '''
            Breaks down the alias string into elements of a list
            '''
            alias_list = []
            word = ""
            for index, letter in enumerate(aliases):
                if index != 0:
                    if letter.isupper() and aliases[index - 1].islower():
                        alias_list.append(word)
                        word = letter
                    else:
                        word += letter
                else:
                    word += letter
                    
            return alias_list
    
    def get_image(self, url):
        """
        Retrieves the image from the url. 
        Save it as a file is it's new.
        returns the filename
        """
        
        file_path = "./images/"+url.split("/")[-1]
        
        if not os.path.exists(file_path):
            
            image = requests.get(url, stream = True)

            if image.status_code == 200:
                image.raw.decode_content = True
                
                with open(file_path,"wb") as file:
                    shutil.copyfileobj(image.raw,file)
                
        return file_path

    # ----- queries ----- #

    def get_last_superhero_id(self):
        '''
        Returns id of last superhero in list
        '''
        self.cursor.execute("""
                            SELECT MAX(super_id)
                            FROM Superhero
                            """)
        results = self.cursor.fetchone()
        return results[0]

    def get_card_details(self, superhero_id):
        '''
        Returns values of a card
        '''
        self.cursor.execute("""
                            SELECT Superhero.super_name, super_intelli, super_stren, super_spd, super_dur, 
                            super_pow, super_comb, super_image
                            FROM Superhero
                            """)
        results = self.cursor.fetchone()
        card_values = list(results)
        card_values.append(self.get_aliases(superhero_id))
        return card_values

    def get_aliases(self, superhero_id):
        """
        returns the aliases of the provided superhero
        in a single string
        """
        self.cursor.execute("""
                            SELECT alias_name
                            FROM Alias
                            WHERE super_id = :superh_id
                            """,
                            {"superh_id":superhero_id})
        results = self.cursor.fetchall()
        if results != []:
            aliases = ""
            for name in results:
                aliases = aliases + name[0] + ", "
            return aliases.rstrip(", ")
        else:
            return None

    def get_max_cards(self):
        """
        Returns the max number of cards excluding all blanks
        """
        total_cards = self.get_last_superhero_id()
        
        self.cursor.execute("""
                            SELECT COUNT(super_name)
                            FROM Superhero
                            WHERE super_intelli is NULL AND
                            super_stren is NULL AND
                            super_spd is NULL AND
                            super_dur is NULL AND
                            super_pow is NULL AND
                            super_comb is NULL
                            """)
        results = self.cursor.fetchone()
        available_cards = total_cards - results[0]
        return(available_cards)

    # ----- inserts ----- #

    def add_superhero(self,vals):
        """
        Adds values into superhero table
        """
        insert_with_param = """INSERT INTO Superhero (
                                super_name,
                                super_intelli,
                                super_stren,
                                super_spd,
                                super_dur,
                                super_pow,
                                super_comb,
                                super_image
                                )
                            VALUES (?,?,?,?,?,?,?,?);"""
        data_tuple = (vals)
        
        self.cursor.execute(insert_with_param,data_tuple)
        self.conn.commit()

    def add_alias(self,vals):
        """
       Adds values into alias table
        """
        insert_with_param = """INSERT INTO Alias (alias_name, super_id)
                            VALUES (?,?);"""
        
        self.cursor.execute(insert_with_param,(vals))
        self.conn.commit()