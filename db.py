
import pyodbc


class Database:
    def __init__(self):
        self.cnxn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                    "Server=DESKTOP-Q3E40OB\SQLEXPRESS;"
                    "Database=EmployeeManagement;"
                    "Trusted_Connection=yes;")
        self.cnxn = pyodbc.connect(self.cnxn_str)
        self.cursor = self.cnxn.cursor()



