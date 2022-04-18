from dataclasses import dataclass
import pymysql
from dataclasses import dataclass


host_address = '13.125.254.122'
@dataclass
class Item:
    brand: str = None
    item_name  :str = None
    item_code :str= None
    main_category : str = None
    sub_category : str = None
    price : int = None
    

def insert(brand, item_name, item_code, main_category, sub_category, price, redirect_url):
    db_con = pymysql.connect(host=host_address,port=3306, user='abletest',passwd='xogus',charset='utf8',db='testdb')
    db_cursor = db_con.cursor()
    insert_sql = 'INSERT INTO item (brand, item_name, item_code, main_category, sub_category, price, redirect_url) VALUES (%s, %s, %s, %s, %s, %s, %s)'
    db_cursor.execute(insert_sql,(brand, item_name, item_code, main_category, sub_category, price, redirect_url))
    db_con.commit()
    db_con.close() 

def search(item_code):
    db_con = pymysql.connect(host=host_address,port=3306, user='abletest',passwd='xogus',charset='utf8',db='testdb')
    db_cursor = db_con.cursor()
    search_sql = 'SELECT * FROM item where item_code = %s'
    db_cursor.execute(search_sql,(item_code))
    res = db_cursor.fetchone()
    db_con.commit()
    db_con.close() 
    if res is not None:
        return Item(res[1],res[2],res[3],res[4],res[5],res[6])
    else:
        return None


if __name__  == '__main__':
    print(search('HC9962'))