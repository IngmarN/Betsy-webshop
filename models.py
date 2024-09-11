import peewee
import uuid

db = peewee.SqliteDatabase("database.db")

class BaseModel(peewee.Model):
    class Meta:
        database = db

class User(BaseModel):
    name = peewee.CharField(unique=True)
    address = peewee.CharField()
    billing_information = peewee.CharField()


class Product(BaseModel):
    name = peewee.CharField()
    description = peewee.CharField()
    price_in_cents = peewee.IntegerField(constraints=[peewee.Check('price_in_cents > 0')])  # Integers won't have rounding errors
    amount_in_stock = peewee.IntegerField(constraints=[peewee.Check('amount_in_stock > -1')])

    class Meta:
        indexes = (
            # Create an index on 'name' and 'description' to speed up search queries
            (('name', 'description'), False),
        )

class UserProduct(BaseModel):
    user = peewee.ForeignKeyField(User, backref='user_products')
    product = peewee.ForeignKeyField(Product, backref='product_users')

    

class Tag(BaseModel):
    name = peewee.CharField(unique=True)


class ProductTag(BaseModel):
    product = peewee.ForeignKeyField(Product, backref='product_tags')
    tag = peewee.ForeignKeyField(Tag, backref='tag_products')


class Transaction(BaseModel):
    transaction_code = peewee.UUIDField(default=uuid.uuid4, unique=True)
    buyer = peewee.ForeignKeyField(User, backref='purchases')
    seller = peewee.ForeignKeyField(User, backref='sales')
    product = peewee.ForeignKeyField(Product, backref='transactions')
    quantity = peewee.IntegerField()
    transaction_date = peewee.DateField(default=peewee.datetime.date.today)


