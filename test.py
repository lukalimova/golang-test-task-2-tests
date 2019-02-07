import psycopg2
import requests
import json
import unittest


class TestCase1(unittest.TestCase):
    connStr = "host='localhost' dbname='db' user='postgres' password='pass'"
    url = 'http://127.0.0.1:8078/get_config'

    def execSql(self, sql):
        conn = psycopg2.connect(self.connStr)
        cursor = conn.cursor()
        # Develop.mr_robot

        # Выполняем запрос.
        cursor.execute(sql)
        #
        row = cursor.fetchone()

        # Закрываем подключение.
        cursor.close()
        conn.close()

        return row

    def test1(self):

        row = self.execSql(
            "SELECT * FROM public.\"develop_mr_robot_configs\" LIMIT 1")

        data = ({"Type": "Develop.mr_robot", "Data": row[0]})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = json.loads(json.dumps({"Data": row[0], "Host": row[1], "Port": row[2],
                                         "Database": row[3], "User": row[4], "Password": row[5], "Schema": row[6]}))
        print(rowjson)
        self.assertEqual(resJson, rowjson)

    def test2(self):

        row = self.execSql("SELECT * FROM public.\"test_vpn_configs\" LIMIT 1")

        data = ({"Type": "Test.vpn", "Data": row[0]})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = json.loads(json.dumps({"Data": row[0], "Host": row[1], "Port": row[2],
                                         "Virtualhost": row[3], "User": row[4], "Password": row[5]}))
        print(rowjson)
        self.assertEqual(resJson, rowjson)


if __name__ == '__main__':
    unittest.main(exit=False)
