import json
import pyodbc
import pandas as pd

class DBExtractor():
    def __init__(self, configFile: str):
        f = open(configFile)
        data = json.load(f)
        
        self._HOST = data["HOST"]
        self._PORT = data["PORT"]
        self._DATABASE = data["DATABASE"]
        self._USER = data["USER"]
        self._PASSWORD = data["PASSWORD"]
        
        f.close()
 

    def extract(self, targetFile: str):
        conn = None
        
        try:
            conn = pyodbc.connect("DRIVER={ODBC Driver 18 for SQL Server}" +
                                ";SERVER=" + self._HOST + 
                                ";DATABASE=" + self._DATABASE + 
                                ";UID=" + self._USER + 
                                ";PWD=" + self._PASSWORD + 
                                ";TrustServerCertificate=Yes")
            
            # Insert your exercise code here
            
            # df = pd.read_sql(......, conn)
            # df.to_csv(......)
            
            # End of exercise
        except:
            print("error extracting data from sqlserver")
        finally:        
            if conn: conn.close()
