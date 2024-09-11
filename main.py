# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
from models import *

# Function that can check a passed in id (like user or product) to see if it exists
def check_id(model, object_id):
    try:
        return model.get(model.id == object_id)
    except model.DoesNotExist:
        raise ValueError(f"{model.__name__} with ID {object_id} does not exist.")


def search(term):
    query = Product.select().where(
        (Product.name.contains(term)) | 
        (Product.description.contains(term))
    )
    matching_products = list(query)

    return matching_products


def list_user_products(user_id):
    query = UserProduct.select().where(
        (UserProduct.user == user_id)
    )
    matching_products = [user_product.product for user_product in query]

    return matching_products


def list_products_per_tag(tag_id):
    query = ProductTag.select().where(ProductTag.tag == tag_id)
    matching_products = [product_tag.product for product_tag in query]

    return matching_products


def add_product_to_catalog(user_id, product_data):
    # Check if user exists by user_id
    user = check_id(User, user_id)

    # Check if user already has product catalogued, error if so
    existing_product = (
        Product.select()
        .join(UserProduct)
        .where((Product.name == product_data['name']) & (UserProduct.user == user_id))
        .first()
    )
    
    if existing_product:
        raise ValueError(f"User already has a product named '{product_data['name']}' in their catalog.")
    


    # Create product
    try:
        product = Product.create(
            name=product_data['name'],
            description=product_data['description'],
            price_in_cents=product_data['price_in_cents'],
            amount_in_stock=product_data['amount_in_stock']
        )
    except peewee.IntegrityError as e:
        raise ValueError(f"Error creating product: {e}")
    

    # Link the product to the user in the UserProduct table
    UserProduct.create(user=user, product=product)

    return product

def remove_product(product_id, user_id):
    # Check if user excists by user_id
    check_id(User, user_id)
    
    # Find the specific UserProduct entry
    query = UserProduct.get_or_none((UserProduct.user == user_id) & (UserProduct.product == product_id))
    
    if query:
        # Delete the entry if found
        query.delete_instance()
        return True  
    else:
        # Return False if the user-product relationship doesn't exist
        return False


def update_stock(product_id, new_quantity):
    # Check if the product exists by product_id
    product = check_id(Product, product_id)

    # Check if the new_quantity isn't negative
    if new_quantity < 0:
        raise ValueError("Stock quantity cannot be negative.")

    # Step 3: Update the stock amount for the product
    product.amount_in_stock = new_quantity
    product.save()  

    return True  # Indicate that the stock was updated


def purchase_product(product_id, buyer_id, seller_id, quantity):
    # Check if the buyer exists
    buyer = check_id(User, buyer_id)

    # Check if the seller exists
    seller = check_id(User, seller_id)

    # Check if the product exists
    product = check_id(Product, product_id)

    # Check if the buyer is not the same as the seller
    if buyer_id == seller_id:
        raise ValueError("Buyer and seller cannot be the same.")

    # Check if the seller has enough stock
    if product.amount_in_stock < quantity:
        raise ValueError(f"Insufficient stock. Only {product.amount_in_stock} units available.")

    # Update the stock for the seller
    new_stock = product.amount_in_stock - quantity
    update_stock(product_id, new_stock)

    # Record the transaction in the Transaction table
    Transaction.create(
        transaction_code=uuid.uuid4(),  # Generate a unique transaction code
        buyer=buyer,
        seller=seller,
        product=product,
        quantity=quantity,
        transaction_date=peewee.datetime.date.today()
    )

    return True  # Indicate the transaction was successful
