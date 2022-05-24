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
            df = pd.read_sql("SELECT c.ItemId, c.ItemDocumentNbr, c.CustomerName, c.CreateDate, c.UpdateDate "
                             "FROM (SELECT Item.*, CustomerName, "
                             "ROW_NUMBER() OVER(PARTITION BY ItemId ORDER BY ItemId,VersionNbr DESC) AS rnum "
                             "FROM Item JOIN Customer ON Item.CustomerId = Customer.CustomerId ) as c "
                             "WHERE rnum<=1 AND c.DeletedFlag = 0;", conn)

            ''''''

            self.add_item_source_column(df)

            df.to_csv(targetFile, ';', '', line_terminator='\r\n', quotechar='"',
                      index=False, encoding='UTF-8', compression='gzip')

            # End of exercise
        except Exception as e:
            print("error extracting data from sqlserver" + e)
        finally:
            if conn: conn.close()

    def add_item_source_column(self, df):
        df['ItemSource'] = ['Local' if (x[-2:] == '66' or x[-2:] == '99')
                            else 'External' for x in df['CustomerName']]