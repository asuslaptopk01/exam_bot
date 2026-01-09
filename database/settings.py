import psycopg2.extras
from dotenv import load_dotenv
load_dotenv()


class CRUD:
    connect = psycopg2.connect(
        dbname=load_dotenv("DB_NAME"),
        host=load_dotenv("DB_HOST"),
        port=load_dotenv("DB_PORT"),
        password=load_dotenv("DB_PASSWORD"),
        user=load_dotenv("DB_USER")
    )
    cursor = connect.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get(self, *cols: object)-> list:
        table_name = self.__class__.__name__.lower() + 's'
        col_format = " , ".join(cols) if cols else "*"
        condition_dict = dict(filter(lambda x : x[1] != None,self.__dict__.items()))
        condition_format = "where "+ " = %s and ".join(condition_dict.keys()) +" = %s" if condition_dict else ""
        query = f"select {col_format} from {table_name} {condition_format}"
        params = tuple(condition_dict.values())
        data: list[dict] = self.get_dict_resultset(query , params)
        objects = []
        for d in data:
            obj = self.__class__(**d)
            objects.append(obj)
        return objects

    def get_dict_resultset(self , query , params = () ):
        self.cursor.execute(query , params)
        ans = self.cursor.fetchall()
        dict_result = []
        for row in ans:
            dict_result.append(dict(row))
        return dict_result

    def delete(self):
        table_name = self.__class__.__name__.lower() + "s"
        condition_dict = dict(filter(lambda x: x[1] != None, self.__dict__.items()))
        condition_format = "where " + " = %s and ".join(condition_dict.keys()) + " = %s" if condition_dict else ""
        params = tuple(condition_dict.values())
        query = f"delete from {table_name} {condition_format}"
        self.cursor.execute(query , params)
        self.connect.commit()

    def update(self, **set_data):
        table_name = self.__class__.__name__.lower() + "s"
        condition_dict = dict(filter(lambda x: x[1] != None, self.__dict__.items()))
        condition_format = "where " + " = %s and ".join(condition_dict.keys()) + " = %s" if condition_dict else ""
        set_format = " =%s , ".join(set_data.keys()) + "=%s"
        params = tuple(list(set_data.values()) + list(condition_dict.values()))
        query = f"update {table_name} set {set_format} {condition_format}"
        self.cursor.execute(query,params)
        self.connect.commit()

    def save(self):
        table_name = self.__class__.__name__.lower() + "s"
        cols_dict = dict(filter(lambda x: x[1] != None, self.__dict__.items()))
        cols_format = " , ".join(cols_dict.keys())
        values_format = " , ".join(["%s"] * len(cols_dict.keys()))
        params = tuple(cols_dict.values())
        query = f"insert into {table_name} ({cols_format}) values ({values_format})"
        self.cursor.execute(query , params)
        self.connect.commit()