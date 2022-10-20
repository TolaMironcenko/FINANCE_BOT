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


class Transaction(BaseModel):
    id = AutoField(column_name='TransactionId')
    type = CharField(column_name='TransactionType', max_length=10, null=False, default='incom')
    sum = FloatField(column_name='TransactionSum', null=False, default=0)
    user = ForeignKeyField(User, unique=True)


conn.create_tables([User, Transaction])