import os
from models import *

def main():
    """
    Comment out the fuction you are not using and run the file.
    """
    populate_database()
    # delete_database()


def populate_database():
    # Connect to the database
    db.connect()
    db.create_tables([User, Product, UserProduct, Tag, ProductTag, Transaction])

    # Create some users
    user1 = User.create(name="Roberto Carlos", address="Dorpsstraat 56", billing_information="Visa 1234")
    user2 = User.create(name="Bob", address="De Brink 2", billing_information="MasterCard 5678")
    user3 = User.create(name="Wolfgang Amadeus Mozart", address="Geheim adres 23", billing_information="PayPal 1212")
    user4 = User.create(name="Donatello the Ninja Turtle", address="Sewers NY", billing_information="Unknown but trustworthy")

    # products
    product1 = Product.create(name="Laptop", description="A high-end candycrush laptop", price_in_cents=150000, amount_in_stock=10)
    product2 = Product.create(name="Smartphone", description="Nokia Ipad pro Max", price_in_cents=80000, amount_in_stock=25)
    product3 = Product.create(name="Headphones", description="Noise-increasing headphones", price_in_cents=20000, amount_in_stock=15)

    # Assign products to users
    UserProduct.create(user=user1, product=product1)
    UserProduct.create(user=user2, product=product2)
    UserProduct.create(user=user3, product=product3)

    #  tags
    tag1 = Tag.create(name="Electronics")
    tag2 = Tag.create(name="Gadgets")
    tag3 = Tag.create(name="Audio")

    # Assign tags to products
    ProductTag.create(product=product1, tag=tag1)
    ProductTag.create(product=product2, tag=tag1)
    ProductTag.create(product=product2, tag=tag2)
    ProductTag.create(product=product3, tag=tag3)

    # transactions
    Transaction.create(buyer=user1, seller=user2, product=product2, quantity=1)
    Transaction.create(buyer=user2, seller=user3, product=product3, quantity=2)
    Transaction.create(buyer=user3, seller=user1, product=product1, quantity=1)
    Transaction.create(buyer=user4, seller=user1, product=product1, quantity=9)

    # Close the database connection
    db.close()


def delete_database():
    """
    Delete the database.
    """
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


if __name__ == "__main__":
    main()