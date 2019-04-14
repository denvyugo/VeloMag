from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, create_engine, ForeignKey
from sqlalchemy.types import DateTime, Float, Integer, String, Boolean, Text, DECIMAL
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class mainapp_product(Base):
    __tablename__ = 'mainapp_product'
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer)
    description = Column(Text)
    image = Column(String(100))
    is_active = Column(Boolean)
    name = Column(String(128))
    price = Column(DECIMAL)
    quantity = Column(Integer)
    short_desc = Column(String(60))

    def __init__(self, category_id, description, image, is_active, name, price, quantity, short_desc):
        self.category_id = category_id
        self.description = description
        self.image = image
        self.is_active = is_active
        self.name = name
        self.price = price
        self.quantity = quantity
        self.short_desc = short_desc

    def __repr__(self):
        return f'<mainapp_product: {self.__tablename__}'


class mainapp_productcategory(Base):
    __tablename__ = 'mainapp_productcategory'
    id = Column(Integer, primary_key = True)
    description = Column(Text)
    is_active = Column(Boolean)
    name = Column(String(64))

    def __init__(self, description, is_active, name):
        self.description = description
        self.is_active = is_active
        self.name = name

    def __repr__(self):
        return f'<mainapp_productcategory: {self.__tablename__}'


engine = create_engine('sqlite:///db.sqlite3', echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

import json

category_ids = {}
q_categories = session.query(mainapp_productcategory).all()
categories = []
for category in q_categories:
    if category.id not in category_ids:
        category_ids[category.id] = category.name
    categories.append({'name': category.name,
                       'description': category.description,
                       'is_active': category.is_active
                       })

with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f)
    
with open('categories.json', 'r', encoding='utf-8') as f:
    print(json.load(f))

q_products = session.query(mainapp_product).all()
products = []
for product in q_products:
    products.append({'name': product.name,
                     'description': product.description,
                     'image': product.image,
                     'price': str(product.price),
                     'quantity': product.quantity,
                     'short_desc': product.short_desc,
                     'category': category_ids[product.category_id],
                     'is_active': product.is_active
                       })

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f)
    
with open('products.json', 'r', encoding='utf-8') as f:
    print(json.load(f))

session.close()

