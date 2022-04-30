from dataclasses import dataclass
from numpy import place
import pymysql
from dataclasses import dataclass


host_address = 'localhost'
@dataclass
class Item:
    brand: str = None
    item_name  :str = None
    item_code :str= None
    main_category : str = None
    sub_category : str = None
    price : int = None
    
@dataclass
class Place:
    place_id:int
    category:str
    place_name:str
    road_address:str
    
    
# 용품 관련 함수===============================================================================================================================================================================================
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

# 장소 관련 함수===============================================================================================================================================================================================
def place_insert(place_id, category, place_name, road_address,place_tel, latitude, longitude, thumnail):
    db_con = pymysql.connect(host=host_address,port=3306, user='abletest',passwd='xogus',charset='utf8',db='testdb')
    db_cursor = db_con.cursor()
    insert_sql = 'INSERT INTO place (place_id, place_category, place_name, road_address, tel, redirect_url, thumbnail_url, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    rUrl = 'm.place.naver.com/place/'+place_id
    db_cursor.execute(insert_sql,(place_id, category, place_name, road_address, place_tel, rUrl, thumnail, latitude, longitude))
    db_con.commit()
    db_con.close() 

def place_search(place_id):
    db_con = pymysql.connect(host=host_address,port=3306, user='abletest',passwd='xogus',charset='utf8',db='testdb')
    db_cursor = db_con.cursor()
    search_sql = 'SELECT * FROM place where place_id = %s'
    db_cursor.execute(search_sql,(place_id))
    res = db_cursor.fetchone()
    db_con.commit()
    db_con.close() 
    if res is not None:
        return Place(res[0],res[1],res[2],res[3])
    else:
        return None

if __name__  == '__main__':
    print(search('HC9962'))