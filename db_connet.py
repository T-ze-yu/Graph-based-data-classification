import pyodbc
import pandas as pd

class getdata_fordb():
    def __init__(self) -> None:
        server = '172.19.1.237,62014'
        username = 'sa'
        password = 'Ceshi123'
        database = 'master'
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
                            'SERVER='+server+';'
                            'DATABASE='+database+';'
                            'UID='+username+';'
                            'PWD='+password+';'
                            'Trusted_Connection=no;') # 连接数据库

    def get_df(self, table, size):
        sql0 = 'SELECT COUNT(1) FROM {}'.format(table)
        # 创建游标
        cursor = self.cnxn.cursor()
        cursor.execute(sql0)
        rows = cursor.fetchone()[0]
        cursor.close()
        
        if rows<=size:
            sql = 'SELECT * FROM {};'.format(table)
        else:
            sql = 'SELECT TOP {} * FROM {} ORDER BY NEWID();'.format(size, table)
        df = pd.read_sql(sql, self.cnxn)
        return df
    
    def close_connect(self):
        self.cnxn.close()
        
if __name__ == '__main__':
    db = getdata_fordb()
    print(db.get_df('R_JOBENTRY_TYPE', 100))
    
    db.cnxn.close()
    