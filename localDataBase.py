import traceback

import sqlite3
from loguru import logger

class SqlLite:
    
    @logger.catch
    def __init__(self, nameDB: str, tableQuery: str):
        self.nameDB = nameDB
        self.conn = sqlite3.connect(nameDB)
        self.cur  = self.conn.cursor()
        try:
            self.cur.execute(tableQuery)
        except Exception as e :
            print('База данных уже создана [выполняеться подключение]', traceback.print_exc())
        self.conn.commit()
    
    def send_values(self, query, values):
        """
            [query]: str - Запрос 
            [values]: list - Данные в томже порядке что и в запросе 
        """
        strVal = "values("    
        for _ in range(len(values)):
                strVal += "?,"
        strVal = strVal[0: -1]
        strVal += ')'
        #strDuplucate = f'ON CONFLICT(id_user) UPDATE set payload = {values[1]}, goloss = {values[2]}'
        self.cur.execute(query + strVal, values)
        self.conn.commit()

    
    @logger.catch
    def send(self, query):
        self.cur.execute(query)
        self.conn.commit()
    
    @logger.catch
    def update(self, query):
        self.cur.execute(query)
        self.conn.commit()

    @logger.catch
    def isHe(self, value, nameTable) -> bool:
        """Проверяет есть ли в базе строка с таким значение"""
        tempVal = self.get(f"select * from {nameTable} where id_user = {value}")
        if tempVal == []:
            return False
        else: 
            return True

    @logger.catch
    def get(self, query):
        a = self.conn.execute(query)
        return list(a)

    @logger.catch
    def get_last_payload(self, user_id, nameTable) -> str:
        lastPayload = self.get(f"select payload from {nameTable} where user_id = {user_id}")
        return list(lastPayload)[0][0]

    def clear_column(self, nameTable):
        self.conn.execute(
        f"""
        DELETE FROM {nameTable} WHERE 1
        """)

sql = SqlLite("Users.db","""
        create table users(
        id integer primary key,
        user_id int unique,
        name text,
        payload text);
        """)

