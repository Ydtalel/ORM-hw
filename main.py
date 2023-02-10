import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import models

from models import *


def json_to_tables():
    with open('data.json', encoding='utf-8') as f:
        data = json.load(f)
        list_of_models = []
        for d in data:
            model = d['model']
            if model == 'publisher':
                name = d['fields']['name']
                publisher = models.Publisher(name=name)
                list_of_models.append(publisher)
            elif model == "book":
                title = d['fields']['title']
                id_publisher = d['fields']['id_publisher']
                book = Book(title=title, id_publisher=id_publisher)
                list_of_models.append(book)
            elif model == "shop":
                name = d['fields']['name']
                shop = models.Shop(name=name)
                list_of_models.append(shop)
            elif model == "stock":
                id_shop = d['fields']['id_shop']
                id_book = d['fields']['id_book']
                count = d['fields']['count']
                stock = Stock(id_shop=id_shop, id_book=id_book, count=count)
                list_of_models.append(stock)
            elif model == "sale":
                price = d['fields']['price']
                date_sale = d['fields']['date_sale']
                count = d['fields']['count']
                id_stock = d['fields']['id_stock']
                sale = Sale(price=price, date_sale=date_sale, count=count, id_stock=id_stock)
                list_of_models.append(sale)
        session.add_all(list_of_models)
        session.commit()


def find_shop_by_publisher(publisher_name):
    q = session.query(Publisher, Book, Stock, Shop).join(Stock.shop).join(Stock.book).join(
        Book.publisher).filter(Publisher.name == publisher_name)
    for el in q:
        for item in el:
            if isinstance(item, Shop):
                print(f" продается в магазине '{item.name}'\n")
            elif isinstance(item, Book):
                print(f"книга '{item.title}'")


def find_sales_information(publisher_=None, id_=None):
    filter_ = ''
    if id_:
        filter_ = Book.id_publisher == id_
    elif publisher_:
        filter_ = Publisher.name == publisher_
    q = session.query(Publisher, Book, Stock, Shop, Sale, ).join(Sale.stock).join(Stock.shop).join(Stock.book).join(
        Book.publisher).filter(filter_)
    for el in q:
        for item in el:
            print(item)


load_dotenv()  # take environment variables from .env.
password = os.getenv('password')
login = os.getenv('login')
database = os.getenv('database')

DSN = f'postgresql://{login}:{password}@localhost:5432/{database}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

json_to_tables()  # Заполняем БД тестовыми данными из data.json
# for item in session.query(Publisher):
#     print(item)
# for item in session.query(Book):
#     print(item)
# for item in session.query(Shop):
#     print(item)
# for item in session.query(Stock):
#     print(item)
# for item in session.query(Sale):
#     print(item)
publisher_name = input('Введите имя издателя: ')
find_shop_by_publisher(publisher_name=publisher_name)  # запрос выборки магазинов, продающих целевого издателя
data = input('Введите имя или идентификатор издателя: ')
try:
    data = int(data)
    find_sales_information(id_=data)  # факты покупки книг издателя
except ValueError:
    find_sales_information(publisher_=data)  # факты покупки книг издателя

session.close()
