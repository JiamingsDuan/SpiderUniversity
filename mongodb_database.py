from pymongo import MongoClient


# 初始化mongodb实体类，存储数据库
class MongoDB:
    def __init__(self, host, db, port=27017):
        """
        :param host: str mongodb地址
        :param db: str 数据库
        :param port: int 端口，默认为27017
        """
        host = host
        db = db
        self.port = port
        client = MongoClient(host=host, port=port)
        self.db = client[db]

    def insert_one(self, table, dic):
        """
        :param table: str 数据库中的集合
        :param dic: dict 要插入的字典
        :return: 返回一个包含ObjectId类型的对象
        """
        collecting = self.db[table]
        response = collecting.insert_one(dic)

        return response
