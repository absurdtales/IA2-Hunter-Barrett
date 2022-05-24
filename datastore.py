import sqlite3
import os
import csv
import requests
import shutil

class SuperheroDB():
    
    def __init__(self):
        
        """
        initialise datastore
        """
        self.filename = "superhero_db.db"
        
        if not os.path.exists(self.filename):
            # if db is not present create it then connect to it
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()
            self.create_superhero_db()
            self.populate_superhero_db()
        else:
            # if db is present connect to it
            self.conn = sqlite3.connect(self.filename)
            self.cursor = self.conn.cursor()
        
    
    def create_superhero_db(self):
        """
        Creates the data structure for the superhero database
        """
        # create publisher table
        self.cursor.execute("""
                            CREATE TABLE Publisher(
                                pub_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL
                            )
                            """)
        
        # create alignment table
        self.cursor.execute("""
                            CREATE TABLE Alignment(
                                align_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL
                            )
                            """)   
        
        
        # create superhero table
        self.cursor.execute("""
                            CREATE TABLE Superhero(
                                super_hero_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                intelligence INTEGER,
                                strength INTEGER,
                                speed INTEGER,
                                durability INTEGER,
                                power INTEGER,
                                combat INTEGER,
                                image TEXT NOT NULL,
                                publisher INTEGER,
                                alignment INTEGER,
                                FOREIGN KEY(publisher) REFERENCES Publisher(pub_id),
                                FOREIGN KEY (alignment) REFERENCES Alignment(align_id)
                            )
                            """)
        
        # create alias id
        self.cursor.execute("""
                            CREATE TABLE Alias(
                                alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL, 
                                superhero INTEGER,
                                FOREIGN KEY(superhero) REFERENCES Superhero(superhero_id)                                
                            )
                            """)


    def populate_superhero_db(self):
        """
        Loads values from superhero.csv into superhero database
        """
        with open("superhero.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for index, hero in enumerate(csv_reader):
                # read the values for a single hero 
                if index > 0:
                    name = hero[0]
                    intel = self.clean_int(hero[1])
                    strgth = self.clean_int(hero[2])
                    speed = self.clean_int(hero[3])
                    dura = self.clean_int(hero[4])
                    power = self.clean_int(hero[5])
                    combat = self.clean_int(hero[6])
                    aliases = hero[9]
                    pub = hero[12]
                    align = hero[13]
                    image = hero[26]
                    
                    # add new published to database and get foreign key
                    if pub != "null" and pub != "":
                        # hero has publisher
                        if self.get_publisher_id(pub) == None:
                            self.add_publisher(pub)
                        pub_id = self.get_publisher_id(pub)
                    else:
                        # hero doesn't have publisher
                        pub_id = None
                    
                    # add new alignment to database and get foreign key
                    if align != "null" and align != "-":
                        # hero has alignment
                        if self.get_alignment_id(align) == None:
                            self.add_alignment(align)
                        align_id = self.get_alignment_id(align)
                    else:
                        # hero doesn't have alignment
                        align_id = None
                    
                    # get image
                    image_path = self.get_image(image)
                    
                    # add superhero to Superhero table
                    self.add_superhero((name,
                                        intel,
                                        strgth,
                                        speed,
                                        dura,
                                        power,
                                        combat,
                                        image_path,
                                        pub_id,
                                        align_id))
                    
                    # process aliases
                    if aliases != "-":
                        sh_id = self.get_last_superhero_id()
                        for alias in self.get_alias_list(aliases):
                            self.add_alias((alias,sh_id))
                            
                        
                    
                
                print(f"{index+1} records processed")
    
                    
    def clean_int(self,val):
        """
        Checks if val is a number or null
        """
        if val == "null":
            return None
        else:
            return int(val)
    
    
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
    
    
    def get_alias_list(self,aliases):
            '''
            Breaks down the alias string into a elements of a list
            A new value is identified by a upper case letter preceeded
            by a lower case letter
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
                    
                    
    # ----- queries ----- #
                       
    def get_publisher_id(self,pub_name):
        """"
        Returns the publisher id for given publisher 
        """
        self.cursor.execute("""
                            SELECT pub_id
                            FROM Publisher
                            WHERE name = :name
                            """,
                            {"name":pub_name}
                            )
        results = self.cursor.fetchall()
        if results == []:
            return None
        else:
            return results[0][0]

    
    def get_alignment_id(self,align_name):
        """"
        Returns the alignment id for given alignment 
        """
        self.cursor.execute("""
                            SELECT align_id
                            FROM Alignment
                            WHERE name = :name
                            """,
                            {"name":align_name}
                            )
        results = self.cursor.fetchall()
        if results == []:
            return None
        else:
            return results[0][0]
    
    
    def get_last_superhero_id(self):
        '''
        returns the id of the last superhero
        '''
        self.cursor.execute("""
                            SELECT MAX(super_hero_id)
                            FROM Superhero
                            """)
        results = self.cursor.fetchone()
        return results[0]
    
    
    def get_card_details(self, superhero_id):
        '''
        returns the values of a card in the form of a list
        '''
        self.cursor.execute("""
                            SELECT Superhero.name, intelligence, strength, speed, durability, 
                            power, combat, image, Publisher.name, Alignment.name
                            FROM Superhero
                            LEFT JOIN Publisher
                            ON Superhero.publisher = Publisher.pub_id 
                            LEFT JOIN Alignment
                            ON Superhero.alignment = Alignment.align_id
                            WHERE Superhero.super_hero_id = :sh_id
                            """,
                            {"sh_id":superhero_id})
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
                            SELECT name
                            FROM Alias
                            WHERE superhero = :sh_id
                            """,
                            {"sh_id":superhero_id})
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
                            SELECT COUNT(name)
                            FROM Superhero
                            WHERE intelligence is NULL AND
                            strength is NULL AND
                            speed is NULL AND
                            durability is NULL AND
                            power is NULL AND
                            combat is NULL
                            """)
        results = self.cursor.fetchone()
        available_cards = total_cards - results[0]
        return(available_cards)
        
        
    # ----- inserts ----- #
    
    def add_publisher(self,pub_name):
        """
        Adds provided publisher to the publisher table
        """
        insert_with_param = """INSERT INTO Publisher (name)
                            VALUES (?);"""
        data_tuple = (pub_name)
        
        self.cursor.execute(insert_with_param,[data_tuple])
        self.conn.commit()

        
    def add_alignment(self,align_name):
        """
        Adds provided alignment to the publisher table
        """
        insert_with_param = """INSERT INTO Alignment (name)
                            VALUES (?);"""
        data_tuple = (align_name)
        
        self.cursor.execute(insert_with_param,[data_tuple])
        self.conn.commit()
        

    def add_superhero(self,vals):
        """
        Adds provided publisher to the publisher table
        """
        insert_with_param = """INSERT INTO Superhero (
                                name,
                                intelligence,
                                strength,
                                speed,
                                durability,
                                power,
                                combat,
                                image,
                                publisher,
                                alignment
                                )
                            VALUES (?,?,?,?,?,?,?,?,?,?);"""
        data_tuple = (vals)
        
        self.cursor.execute(insert_with_param,data_tuple)
        self.conn.commit()
        
    
    def add_alias(self,vals):
        """
        Adds provided publisher to the publisher table
        """
        insert_with_param = """INSERT INTO Alias (name,superhero)
                            VALUES (?,?);"""
        
        self.cursor.execute(insert_with_param,(vals))
        self.conn.commit()