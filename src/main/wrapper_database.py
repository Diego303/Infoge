import sqlite3

class wrapper_database:
  
    def __init__(self):
        self.sqliteConnection = None
        self.cursor = None
        
        
# -- Comprobar Login de un Usuario -- 
    def login_user(self,user,password):
        self.sqliteConnection = sqlite3.connect('infoge.db')
        self.cursor = self.sqliteConnection.cursor()
        
        self.cursor.execute("SELECT * FROM usuarios where email='"+user+"' and password='"+password+"'")
        ans = self.cursor.fetchall()
        user_existente=True
        if len(ans) ==0:
            user_existente=False

        self.sqliteConnection.close()
        return user_existente


