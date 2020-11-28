import pymysql
from elasticsearch import Elasticsearch


class MySql:
    def __init__(self, host: str, db: str, user: str, password: str):
        self._host = host
        self._db = db
        self._user = user
        self._password = password

    def __connect__(self):
        self.con = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            db=self._db,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()

    def multi_execute(self, sql: [str]):
        self.__connect__()
        statements = sql.split(";")[:-1]
        results = []
        for statement in statements:
            self.cur.execute(statement)
            self.con.commit()
            results.append(self.cur.fetchall())
        self.__disconnect__()
        return results


class ES:
    def __init__(self, host: str, port: int):
        self._es = Elasticsearch([{"host": host, "port": port}])

    def store_record(self, index_name: str, record: dict, doc_type: str):
        self._es.index(index=index_name, body=record, doc_type=doc_type)

    def delete_record(self, index_name: str, doc_type: str, query: dict):
        self._es.delete_by_query(index=index_name, doc_type=doc_type, query=query)
