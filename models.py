import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(length=50), unique=True, nullable=False)

    def __str__(self):
        return f"{self.name} - Имя издателя"


class Book(Base):
    __tablename__ = 'book'

    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(length=75), nullable=False)
    id_publisher = sql.Column(sql.Integer, sql.ForeignKey('publisher.id'), nullable=False)

    def __str__(self):
        return f"{self.title} - Название книги"

    publisher = relationship(Publisher, backref='books')


class Shop(Base):
    __tablename__ = 'shop'

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(length=30), unique=True, nullable=False)

    def __str__(self):
        return f"{self.name} - Название магазина"


class Stock(Base):
    __tablename__ = 'stock'

    id = sql.Column(sql.Integer, primary_key=True)
    count = sql.Column(sql.Integer)
    id_book = sql.Column(sql.Integer, sql.ForeignKey('book.id'), nullable=False)
    id_shop = sql.Column(sql.Integer, sql.ForeignKey('shop.id'), nullable=False)

    def __str__(self):
        return f"{self.count} - Количество книг на складе"

    shop = relationship(Shop, backref='stocks')
    book = relationship(Book, backref='stocks')


class Sale(Base):
    __tablename__ = 'sale'

    id = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column(sql.Float, nullable=False)
    count = sql.Column(sql.Integer, nullable=False)
    date_sale = sql.Column(sql.Date, nullable=False)
    id_stock = sql.Column(sql.Integer, sql.ForeignKey('stock.id'), nullable=False)

    def __str__(self):
        return f"{self.price} - Цена продажи, {self.date_sale} - Дата продажи"

    stock = relationship(Stock, backref='sales')


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
