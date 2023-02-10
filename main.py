import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from models import *


def json_to_tables():
    with open('data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
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
    if id_:
        filter_ = Book.id_publisher == id_
    elif publisher_:
        filter_ = Publisher.name == publisher_
    res = session.query(Book.title, Shop.name, Sale.price, Sale.count, Sale.date_sale). \
        join(Publisher).join(Stock).join(Sale).join(Shop).filter(filter_)

    for book, shop, price, count, date in res:
        print(f'{book: <40} | {shop: <10} | {price * count: <8} | {date}')


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
