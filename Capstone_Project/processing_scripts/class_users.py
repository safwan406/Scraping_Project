import sqlite3

class Users:
    """ This class is used to access the Database of users """

    def __init__(self, db): # call class this extecuted itself
        """ 
        This function creates a connection to the Database
        
        Args:
            db (str): name of the database to access
        """

        self.conn = sqlite3.connect(db, check_same_thread = False) # created a connection to database
        self.cur = self.conn.cursor() # keeps track of the position in the result set
        self.cur.execute("CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY, name TEXT UNIQUE, password TEXT)")
        self.conn.commit()

    def inserting(self, userName, password):
        """ 
        This function inserts new entries into the Database 
        
        Args:
            userName (str): name of the user
            password (str): password for the user
        """

        self.cur.execute("INSERT INTO subscribers VALUES (NULL, ?, ?)" , (userName, password))
        self.conn.commit() #committing the current transaction
        print(userName, password)

    def search(self, userName, password):
        """ 
        This function inserts new entries into the Database 
        
        Args:
            userName (str): name of the user
            password (str): password for the user

        Returns:
            row : entry found against passed arguments from database
        """
        self.cur.execute('SELECT * FROM subscribers WHERE name = ? AND password = ?', (userName, password))
        print("here")
        row = self.cur.fetchone()
        return row
