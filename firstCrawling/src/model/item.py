from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String,Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session

DATABASES = create_engine('mysql+pymysql://abletest:xogus@localhost:3306/testdb?charset=utf8', echo = False)

Base = declarative_base()
class Item(Base):
    __tablename__ = 'item'
    
    id = Column('item_id', Integer,primary_key=True)
    name = Column('item_name', String(255))
    code = Column('item_code', String(255))
    price = Column('price', Integer)
    redirect_url = Column('redirect_url',String(255))
    main_category = Column('main_category', String(255))
    sub_category = Column('sub_category', String(255))
    brand1 = Column('brand_1', Integer)
    brand2 = Column('brand_2', Integer)
    brand3 = Column('brand_3', Integer)
    brand4 = Column('brand_4', Integer)
    brand5 = Column('brand_5', Integer)     
    
    def __repr__(self) -> str:
        return 'Item<{0} {1} {2} {3} {4} {5} {6}>'.format(
            self.id, self.name, self.code, self.brand1, self.brand2, self.brand3, self.brand4    
        )
    
    
    
def searchItemByCode(item_code:str) -> Item:
    session = sessionmaker(bind=DATABASES)
    result = session.query(Item).filter(Item.code == item_code).first()
    
    session.close()
    
    return result

def addBrandByItemCode(item_code:str, brand_id:int):
    session = scoped_session(sessionmaker(bind=DATABASES)) 

    result = session.query(Item).filter(Item.code == item_code).first()
    if(result == None):
        print(item_code,": 해당 제품이 존재하지않습니다.")
        session.close()
        return
    
    brand_arr = list(filter(None, [result.brand1,result.brand2,result.brand3,result.brand4,result.brand5]))
    brand_arr.append(brand_id)
    brand_arr = list(set(brand_arr)) #중복제거
    brand_arr.sort()
    
    try:
        result.brand1 = brand_arr.pop(0)
        result.brand2 = brand_arr.pop(0)
        result.brand3 = brand_arr.pop(0)
        result.brand4 = brand_arr.pop(0)
        result.brand5 = brand_arr.pop(0)
    except:
        pass
    finally:
        session.commit()
        print(item_code,':',result)
        session.close()

addBrandByItemCode('GL8761',1)