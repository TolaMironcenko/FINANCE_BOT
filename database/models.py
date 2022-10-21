import datetime

from peewee import *
from .base import conn


# базовая можель от которой наследуются остальные
class BaseModel(Model):
    class Meta:
        database = conn


# модель пользователя
class User(BaseModel):
    id = AutoField(column_name='UserId')
    username = CharField(column_name='Username', max_length=100, null=False)
    balance = FloatField(column_name='Balance', null=False, default=0)

    class Meta:
        table_name = 'User'


# модель транзакции
class Transaction(BaseModel):
    id = AutoField(column_name='TransactionId')
    type = CharField(column_name='TransactionType', max_length=10, null=False, default='incom')
    sum = FloatField(column_name='TransactionSum', null=False, default=0)
    user = ForeignKeyField(User, unique=False)
    date = DateField(column_name='Date', default=datetime.datetime.today())
    time = TimeField(column_name='time', default=datetime.datetime.now())
    category = TextField(column_name='category', default='None category')

    class Meta:
        table_name = 'Transaction'


class Check(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name', max_length=50, null=False, default='check')
    balance = FloatField(column_name='balance', null=False, default=0)
    user = ForeignKeyField(User, unique=False)


# создаю таблицы
conn.create_tables([User, Transaction])
