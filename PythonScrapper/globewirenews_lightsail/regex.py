
import mysql.connector as mysqldb

def db_conn():
    ''' DataBase Connection '''
    try:
        connection = mysqldb.connect(host="ls-16690a180e0a6fd4b048227253a3ef5e682b6253.cfxfiziytxdd.us-east-1.rds.amazonaws.com", port=3306, database="scrapper", user="dbmasteruser", password="hT(_ZaIBhop,fCrTJ?x=7#g?rX.Aw$lS", autocommit=True)
    except Exception as err:
        connection = mysqldb.connect(host="ls-16690a180e0a6fd4b048227253a3ef5e682b6253.cfxfiziytxdd.us-east-1.rds.amazonaws.com", port=3306, database="scrapper", user="dbmasteruser", password="hT(_ZaIBhop,fCrTJ?x=7#g?rX.Aw$lS", autocommit=True)
        print(err)
    return connection

conn = db_conn()
cur = conn.cursor()

cur.execute("TRUNCATE TABLE dataset")
cur.execute("TRUNCATE TABLE datacheck")
# import requests

# API_ENDPOINT = "https://hooks.zapier.com/hooks/catch/5556991/ouqpzyd/"
# data = {"data":{"Data Company Title":"entry","Data News":"entry[1]","Data Timestamp":"entry[2]"}}
# headers = {'content-type': 'application/json'}
# requests.post(url = API_ENDPOINT, json= data, headers=headers)