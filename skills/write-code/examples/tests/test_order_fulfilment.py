"""Exercise reservation behaviour through the inventory's public interface."""

from collections.abc import Callable

import pytest

from order_fulfilment import (
    InsufficientStock,
    InvalidReservationState,
    Inventory,
    Order,
    OrderLine,
    Reservation,
    ReservationStatus,
)

Transition = Callable[[Inventory, str], Reservation]


def test_failed_reservation_does_not_partially_hold_stock() -> None:
    inventory = Inventory({"BOOK": 5, "PEN": 1})
    order = Order("order-1", (OrderLine("BOOK", 2), OrderLine("PEN", 2)))

    with pytest.raises(InsufficientStock, match="PEN"):
        inventory.reserve(order)

    assert inventory.available_units("BOOK") == 5
    assert inventory.available_units("PEN") == 1
    with pytest.raises(KeyError):
        inventory.get_reservation("order-1")


def test_cancellation_releases_all_held_stock() -> None:
    inventory = Inventory({"BOOK": 5, "PEN": 3})
    original = inventory.reserve(
        Order("order-1", (OrderLine("BOOK", 2), OrderLine("PEN", 3)))
    )
    assert inventory.available_units("BOOK") == 3
    assert inventory.available_units("PEN") == 0

    cancelled = inventory.cancel("order-1")

    assert cancelled.status is ReservationStatus.CANCELLED
    assert inventory.get_reservation("order-1") == cancelled
    assert inventory.available_units("BOOK") == 5
    assert inventory.available_units("PEN") == 3
    assert original.status is ReservationStatus.RESERVED


def test_shipping_does_not_deduct_reserved_stock_twice() -> None:
    inventory = Inventory({"BOOK": 5})
    inventory.reserve(Order("order-1", (OrderLine("BOOK", 2),)))

    shipped = inventory.ship("order-1")

    assert shipped.status is ReservationStatus.SHIPPED
    assert inventory.get_reservation("order-1") == shipped
    assert inventory.available_units("BOOK") == 3


@pytest.mark.parametrize("complete", [Inventory.ship, Inventory.cancel])
@pytest.mark.parametrize("next_transition", [Inventory.ship, Inventory.cancel])
def test_completed_reservations_cannot_change_again(
    complete: Transition, next_transition: Transition
) -> None:
    inventory = Inventory({"BOOK": 5})
    inventory.reserve(Order("order-1", (OrderLine("BOOK", 2),)))
    completed = complete(inventory, "order-1")
    available = inventory.available_units("BOOK")

    with pytest.raises(InvalidReservationState):
        next_transition(inventory, "order-1")

    assert inventory.get_reservation("order-1") == completed
    assert inventory.available_units("BOOK") == available


@pytest.mark.parametrize("complete", [None, Inventory.ship, Inventory.cancel])
def test_order_identifiers_cannot_be_reused(complete: Transition | None) -> None:
    inventory = Inventory({"BOOK": 5})
    order = Order("order-1", (OrderLine("BOOK", 2),))
    inventory.reserve(order)
    if complete is not None:
        complete(inventory, "order-1")
    available = inventory.available_units("BOOK")

    with pytest.raises(ValueError, match="already been reserved"):
        inventory.reserve(order)

    assert inventory.available_units("BOOK") == available


def test_reserved_stock_is_unavailable_to_other_orders() -> None:
    inventory = Inventory({"BOOK": 3})
    inventory.reserve(Order("order-1", (OrderLine("BOOK", 2),)))
    second = Order("order-2", (OrderLine("BOOK", 2),))
    with pytest.raises(InsufficientStock):
        inventory.reserve(second)

    inventory.cancel("order-1")
    reservation = inventory.reserve(second)

    assert reservation.status is ReservationStatus.RESERVED
    assert inventory.available_units("BOOK") == 1


def test_unknown_products_have_no_available_stock() -> None:
    inventory = Inventory({})

    assert inventory.available_units("UNKNOWN") == 0
    with pytest.raises(InsufficientStock):
        inventory.reserve(Order("order-1", (OrderLine("UNKNOWN", 1),)))


@pytest.mark.parametrize(
    "look_up", [Inventory.get_reservation, Inventory.ship, Inventory.cancel]
)
def test_unknown_reservations_raise_key_error(look_up: Transition) -> None:
    with pytest.raises(KeyError):
        look_up(Inventory({}), "unknown")


def test_inventory_copies_its_starting_stock() -> None:
    stock = {"BOOK": 5}
    inventory = Inventory(stock)
    stock["BOOK"] = 100

    assert inventory.available_units("BOOK") == 5


def test_negative_stock_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        Inventory({"BOOK": -1})


@pytest.mark.parametrize("quantity", [0, -1])
def test_order_lines_require_a_positive_quantity(quantity: int) -> None:
    with pytest.raises(ValueError):
        OrderLine("BOOK", quantity)


def test_orders_require_nonempty_unique_lines() -> None:
    with pytest.raises(ValueError, match="at least one line"):
        Order("order-1", ())
    with pytest.raises(ValueError, match="repeated SKUs"):
        Order("order-1", (OrderLine("BOOK", 2), OrderLine("BOOK", 2)))
