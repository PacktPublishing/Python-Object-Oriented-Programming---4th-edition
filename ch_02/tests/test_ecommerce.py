"""
Python 3 Object-Oriented Programming

Chapter 2, Objects in Python.
"""

from ecommerce.products import Product
import ecommerce.products
import ecommerce.payments.stripe

def test_products_db_1():
    db = ecommerce.products.database.Database("path/to/data")
    assert db.fetch("test_1") == {'key': 'test_1'}

def test_products_db_2():
    db = ecommerce.products.Database("path/to/data")
    assert db.fetch("test_2") == {'key': 'test_2'}

def test_products_db_3():
    db = ecommerce.products.DB("path/to/data")
    assert db.fetch("test_3") == {'key': 'test_3'}

def test_products_db_4():
    db = ecommerce.products.DB("path/to/data")
    q = ecommerce.products.Query(db, "products")

def test_products_db_5():
    ecommerce.products.database.initialize_database("production/data")
    assert ecommerce.products.database.db.connection ==  'production/data'

def test_products_db_6():
    db = ecommerce.products.database.get_database("production/data")
    assert db.connection ==  'production/data'

def test_payments_db():
    assert ecommerce.payments.stripe.payment() == {"key": "test_2"}
