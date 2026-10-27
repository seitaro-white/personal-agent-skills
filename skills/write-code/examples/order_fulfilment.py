"""Model stock reservations without coupling business rules to a CLI or database.

Inventory owns available stock and the reservation lifecycle. Reserving an order
holds every requested item or changes nothing. Cancellation releases held stock;
shipping consumes it. Completed reservations remain visible and cannot be reused.

This is an in-memory, single-threaded model. A database-backed service would need
transactional storage for these same guarantees across concurrent requests.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum


class InsufficientStock(ValueError):
    """An order cannot be reserved in full using the available stock."""


class InvalidReservationState(ValueError):
    """A completed reservation cannot be shipped or cancelled again."""


class ReservationStatus(StrEnum):
    """The lifecycle states of a stock reservation."""

    RESERVED = "reserved"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderLine:
    """A positive quantity of one product requested by an order."""

    sku: str
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("order quantity must be positive")


@dataclass(frozen=True)
class Order:
    """A non-empty order with at most one line per product."""

    order_id: str
    lines: tuple[OrderLine, ...]

    def __post_init__(self) -> None:
        if not self.lines:
            raise ValueError("an order must contain at least one line")
        # Repeated SKUs would each pass the stock check alone but overdraw together.
        if len({line.sku for line in self.lines}) != len(self.lines):
            raise ValueError("combine repeated SKUs into a single order line")


@dataclass(frozen=True)
class Reservation:
    """An immutable snapshot of an order and its status when it was returned."""

    order: Order
    status: ReservationStatus


class Inventory:
    """Own available stock and transitions between reservation states."""

    def __init__(self, available_units: Mapping[str, int]) -> None:
        """Create an inventory with no reservations.

        Args:
            available_units: Units available for each SKU; copied, not shared.

        Raises:
            ValueError: Any SKU has a negative number of units.
        """
        if any(units < 0 for units in available_units.values()):
            raise ValueError("available units must not be negative")
        self._available_units = dict(available_units)
        self._reservations: dict[str, Reservation] = {}

    def available_units(self, sku: str) -> int:
        """Return units not held by reservations, or zero for an unknown SKU."""
        return self._available_units.get(sku, 0)

    def get_reservation(self, order_id: str) -> Reservation:
        """Return the current reservation, including shipped or cancelled orders.

        Raises:
            KeyError: The order has never been reserved.
        """
        return self._reservations[order_id]

    def reserve(self, order: Order) -> Reservation:
        """Hold every item in an order, or change nothing if any item is short.

        Raises:
            ValueError: The order ID has already been used, even if completed.
            InsufficientStock: One or more products have insufficient stock.
        """
        if order.order_id in self._reservations:
            raise ValueError(f"order {order.order_id!r} has already been reserved")
        # Check the whole order before changing any stock: partial holds are forbidden.
        shortages = [
            line.sku
            for line in order.lines
            if self.available_units(line.sku) < line.quantity
        ]
        if shortages:
            raise InsufficientStock(f"insufficient stock for: {', '.join(shortages)}")

        for line in order.lines:
            self._available_units[line.sku] -= line.quantity
        return self._record(order, ReservationStatus.RESERVED)

    def cancel(self, order_id: str) -> Reservation:
        """Cancel an active reservation and make its stock available again.

        Raises:
            KeyError: The order has never been reserved.
            InvalidReservationState: The reservation is already shipped or cancelled.
        """
        order = self._require_reserved(order_id)
        for line in order.lines:
            self._available_units[line.sku] += line.quantity
        return self._record(order, ReservationStatus.CANCELLED)

    def ship(self, order_id: str) -> Reservation:
        """Mark an active reservation as shipped; its stock was deducted on reserving.

        Raises:
            KeyError: The order has never been reserved.
            InvalidReservationState: The reservation is already shipped or cancelled.
        """
        order = self._require_reserved(order_id)
        return self._record(order, ReservationStatus.SHIPPED)

    def _require_reserved(self, order_id: str) -> Order:
        reservation = self.get_reservation(order_id)
        if reservation.status is not ReservationStatus.RESERVED:
            raise InvalidReservationState(
                f"order {order_id!r} is already {reservation.status}"
            )
        return reservation.order

    def _record(self, order: Order, status: ReservationStatus) -> Reservation:
        reservation = Reservation(order=order, status=status)
        self._reservations[order.order_id] = reservation
        return reservation
