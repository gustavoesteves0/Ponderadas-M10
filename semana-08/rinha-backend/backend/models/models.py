from typing import Optional
from ormar import Integer, String, ForeignKey, Float, Model
import datetime
from database.postgres import base_ormar_config


class User(Model):
    ormar_config = base_ormar_config.copy(tablename="user")

    id = Integer(primary_key=True, autoincrement=True)
    name = String(max_length=100)
    email = String(max_length=100, unique=True, index=True)
    password = String(max_length=100)


class Transaction(Model):
    ormar_config = base_ormar_config.copy(tablename="transaction")

    id = Integer(primary_key=True, autoincrement=True)
    amount = Float(nullable=False)
    timestamp = String(nullable=False, max_length=100)
    status = String(max_length=20, default="pending")

    user: Optional[User] = ForeignKey(User)

