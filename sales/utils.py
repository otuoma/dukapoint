from importlib import import_module
from django.conf import settings

session = import_module(settings.SESSION_ENGINE).SessionStore()

session['cart_products'] = []


def cart_products():

    products_in_cart = []

    for product in session['cart_products']:

        try:
            products_in_cart.append(product['product_id'])
        except KeyError:
            continue

    return products_in_cart


def update_cart(product_id, new_qty, new_price):

    for product in session['cart_products']:

        try:

            if product['product_id'] == product_id:

                # Update qty, price and total price
                product['quantity'] = new_qty
                product['price'] = new_price
                product['total'] = product['quantity'] * product['price']

            else:
                continue
        except KeyError:
            continue

    return None


def add_to_cart(new_product):

    if new_product['product_id'] not in cart_products():

        session['cart_products'].append(new_product)

    else:

        update_cart(
            new_product['product_id'],
            new_product['quantity'],
            new_product['price']
        )

    session.create()

    return session['cart_products']

