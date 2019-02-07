import psycopg2
import requests
import json
import unittest
import random
import string

class golangTestCase(unittest.TestCase):
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

    def testSunDayMr_robot_configs(self):

        row = self.execSql(
            "SELECT * FROM public.\"develop_mr_robot_configs\" LIMIT 1")

        data = ({"Type": "Develop.mr_robot", "Data": row[0]})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = json.loads(json.dumps({"Data": row[0], "Host": row[1], "Port": row[2],
                                         "Database": row[3], "User": row[4], "Password": row[5], "Schema": row[6]}))
        self.assertEqual(resJson, rowjson)

    def testRainDayMr_robot_configs(self):
        badData = ''.join([random.choice(string.ascii_letters) for n in range(7)])

        row = self.execSql(
            "SELECT * FROM public.\"develop_mr_robot_configs\" WHERE data ='%s'" % badData)
        data = ({"Type": "Develop.mr_robot", "Data": badData})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = {"error": "record not found"}
        self.assertEqual(row, None) 
        self.assertEqual(resJson, rowjson)    

    def testSunDayVpn_configs(self):

        row = self.execSql("SELECT * FROM public.\"test_vpn_configs\" LIMIT 1")

        data = ({"Type": "Test.vpn", "Data": row[0]})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = json.loads(json.dumps({"Data": row[0], "Host": row[1], "Port": row[2],
                                         "Virtualhost": row[3], "User": row[4], "Password": row[5]}))
        self.assertEqual(resJson, rowjson)

    def testRainDayVpn_configs(self):
        badData = ''.join([random.choice(string.ascii_letters) for n in range(7)])

        row = self.execSql(
            "SELECT * FROM public.\"test_vpn_configs\" WHERE data ='%s'" % badData)
        data = ({"Type": "Test.vpn", "Data": badData})
        res = requests.post(self.url, json=data)
        resJson = json.loads(res.text)

        rowjson = {"error": "record not found"}
        self.assertEqual(row, None) 
        self.assertEqual(resJson, rowjson)  

if __name__ == '__main__':
    unittest.main(exit=False)
