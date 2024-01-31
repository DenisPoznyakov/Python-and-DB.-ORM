import sqlalchemy as sq
import json
import psycopg2
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

DSN = 'postgresql://postgres:padzzzer18flot18vk@localhost:5432/ormm'
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='book')

    def __str__(self):
        return f'{self.title}'

class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)

    def __str__(self):
        return f'{self.name}'

class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    book = relationship(Book, backref='stock')
    shop = relationship(Shop, backref='stock')

class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(10,2), nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    stock = relationship(Stock, backref='sale')

    def __str__(self):
        return f'{self.price} | {self.date_sale}'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def loading_data():
    with open('fixtures/tests_data.json', 'r') as fd:
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

def search_publisher(request_publisher):
    result = session.query(Book, Shop, Sale).filter(Publisher.name == request_publisher).filter(Publisher.id == Book.id_publisher).filter(Book.id_publisher == Stock.id_book).filter(Stock.id_shop == Shop.id).filter(Stock.id == Sale.id_stock).all()
    for i in result:
        print(f'{i[0]} | {i[1]} | {i[2]}')

# create_tables(engine)
# loading_data()

# search_publisher('O\u2019Reilly')
# search_publisher('Pearson')
# search_publisher('Microsoft Press')
# search_publisher('No starch press')

session.close()