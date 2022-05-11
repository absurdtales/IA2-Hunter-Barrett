import sqlite3
import os
import csv
PATH = "./"
DB_FILE = PATH + "fitness.db"
def create_table(sql_command):
    # create a table within the database
    with sqlite3.connect(DB_FILE) as database:
        cursor = database.cursor()
        cursor.execute(sql_command)

def create_database():
    # create classes table
    classes_table = """
                    CREATE TABLE Classes(
                        activity TEXT PRIMARY KEY,
                        instructor TEXT NOT NULL,
                        max_size INTEGER NOT NULL
                    );
                    """
    create_table(classes_table)
    # create sexes table
    sexes_table =   """
                    CREATE TABLE Sexes (
                        sex TEXT PRIMARY KEY,
                        sex_name TEXT NOT NULL
                    );
                    """
    create_table(sexes_table)
    # create weight table
    weight_table =  """
                    CREATE TABLE Weight (
                        height INTEGER PRIMARY KEY,
                        max_weight INTEGER NOT NULL,
                        min_weight INTEGER NOT NULL
                    );
                    """
    # create clients table
    clients_table = """
                    CREATE TABLE Clients (
                        id_number INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        street TEXT NOT NULL,
                        town TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        activity TEXT NOT NULL,
                        sex TEXT NOT NULL,
                        height INTEGER NOT NULL,
                        FOREIGN KEY (activity)
                            REFERENCES Classes (activity)
                        FOREIGN KEY (sex)
                            REFERENCES Sexes (sex)
                        FOREIGN KEY (height)
                            REFERENCES Weight (height)
                    );
                    """
    create_table(clients_table)
    # create readings table
    readings_table =    """
                        CREATE TABLE Readings (
                            id_number INTEGER NOT NULL,
                            month TEXT NOT NULL,
                            RHR INTEGER NOT NULL,
                            weight INTEGER NOT NULL,
                            PRIMARY KEY(id_number,month)
                        );
                        """
    create_table(readings_table)

def process_record(record):
    # accept a list of variables and return a string for SQL
    #print(record)
    new_record = ""
    for item in record:
        if item.isdigit():
            new_record = new_record + item + ","
        else:
            new_record = new_record + "'" + item + "',"
    return new_record[:-1]

def parse_csv(file_name, table):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        for row in csv_reader:
            values = process_record(row)
            insert_values = f"""
                            INSERT INTO {table}
                            VALUES ({values})
                                """
            #print(insert_values)
            sql_command(insert_values)

def import_csv():
    # extracts the data from provided CSV files and enters into the database
    print("here")
    parse_csv(PATH + "/CSV Files/tblClasses.csv", "Classes")
    parse_csv(PATH + "/CSV Files/tblSexes.csv", "Sexes")
    parse_csv(PATH + "/CSV Files/tblWeight_Chart.csv", "Weight")
    parse_csv(PATH + "/CSV Files/tblClients.csv", "Clients")
    parse_csv(PATH + "/CSV Files/tblReadings.csv", "Readings")

def query_db():
    # runs the given query on the database
    pass

def export_csv():
    # saves the proved data to CSV file
    pass

# --- MAIN PROGRAM ---
if not os.path.exists(DB_FILE):
    create_database()
    import_csv()
