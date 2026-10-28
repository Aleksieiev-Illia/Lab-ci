from unittest.mock import Mock

import pytest
from shop.cart import Cart, Item


def test_cart_initial_empty(empty_cart: Cart) -> None:
    assert empty_cart.items_count() == 0
    assert empty_cart.total() == 0.0


def test_add_item(empty_cart: Cart) -> None:
    empty_cart.add("apple", 10.0, 5)
    assert empty_cart.items_count() == 5
    assert empty_cart.total() == 50.0


def test_add_existing_item_increases_qty(empty_cart: Cart) -> None:
    empty_cart.add("apple", 10.0, 2)
    empty_cart.add("apple", 10.0, 3)
    assert empty_cart.items_count() == 5
    assert empty_cart.total() == 50.0


def test_remove_item(cart_with_items: Cart) -> None:
    cart_with_items.remove("pen")
    assert cart_with_items.items_count() == 2
    assert cart_with_items.total() == 400.0


def test_remove_non_existent_item_raises(empty_cart: Cart) -> None:
    with pytest.raises(KeyError, match="notebook"):
        empty_cart.remove("notebook")


def test_add_negative_price_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="price must be non-negative"):
        empty_cart.add("banana", -5.0, 1)


def test_add_non_positive_qty_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("banana", 10.0, 0)
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("banana", 10.0, -2)


@pytest.mark.parametrize(
    ("discount", "expected_total"),
    [
        (0, 460.0),
        (10, 414.0),
        (50, 230.0),
        (100, 0.0),
    ],
)
def test_total_with_discounts(
    cart_with_items: Cart, discount: float, expected_total: float
) -> None:
    assert cart_with_items.total(discount) == pytest.approx(expected_total)


@pytest.mark.parametrize("invalid_discount", [-1.0, 100.1, -0.01])
def test_total_invalid_discount_raises(
    cart_with_items: Cart, invalid_discount: float
) -> None:
    with pytest.raises(ValueError, match=r"discount_percent must be in \[0, 100\]"):
        cart_with_items.total(invalid_discount)


def test_total_in_currency_success(cart_with_items: Cart) -> None:
    rates_mock = Mock()
    rates_mock.get_rate.return_value = 40.0
    assert cart_with_items.total_in("USD", rates_mock) == 11.5
    rates_mock.get_rate.assert_called_once_with("USD")


def test_total_in_currency_invalid_rate_raises(cart_with_items: Cart) -> None:
    rates_mock = Mock()
    rates_mock.get_rate.return_value = 0.0
    with pytest.raises(ValueError, match="rate must be positive"):
        cart_with_items.total_in("EUR", rates_mock)


def test_most_expensive_empty_cart(empty_cart: Cart) -> None:
    assert empty_cart.most_expensive() is None


def test_most_expensive_with_items(cart_with_items: Cart) -> None:
    most_exp = cart_with_items.most_expensive()
    assert most_exp is not None
    assert most_exp.name == "book"
    assert most_exp.price == 200.0


def test_most_expensive_multiple_items(empty_cart: Cart) -> None:
    empty_cart.add("pen", 10.0, 1)
    empty_cart.add("notebook", 50.0, 1)
    item = empty_cart.most_expensive()
    assert item == Item(name="notebook", price=50.0, qty=1)