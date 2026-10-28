import pytest
from shop.cart import Cart


@pytest.fixture
def empty_cart() -> Cart:
    return Cart()


@pytest.fixture
def cart_with_items() -> Cart:
    cart = Cart()
    cart.add("book", 200.0, 2)
    cart.add("pen", 15.0, 4)
    return cart