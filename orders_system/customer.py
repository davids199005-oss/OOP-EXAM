from orders_system.enums import CustomerType
from orders_system.interfaces import Gift
from orders_system.order_item import OrderItem
from orders_system.exceptions import DuplicateIdError


class Customer:
    """A website customer. Each customer has a unique id."""

    _used_ids: set[int] = set[int]()

    def __init__(
        self,
        customer_id: int,
        first_name: str,
        last_name: str,
        email: str,
        delivery_address: str,
        customer_type: CustomerType,
        customer_discount: float | None = None,
    ) -> None:
        self._validate_id(customer_id)
        self._validate_discount(discount=customer_discount)

        Customer._used_ids.add(customer_id)
        self._id: int = customer_id
        self._first_name: str = first_name
        self._last_name: str = last_name
        self._email: str = email
        self._delivery_address: str = delivery_address
        self._customer_type: CustomerType = customer_type
        self._customer_discount: float | None = customer_discount
        self._favorite_items: list[OrderItem] = []
        self._gift: Gift | None = None

    @staticmethod
    def _validate_id(customer_id: int) -> None:
        if customer_id in Customer._used_ids:
            raise DuplicateIdError(entity="Customer", entity_id=customer_id)

    @staticmethod
    def _validate_discount(discount: float | None) -> None:
        if discount is None:
            return
        if not 0 <= discount <= 100:
            raise ValueError(f"Discount must be in range 0..100, got {discount}")

    @property
    def id(self) -> int:
        return self._id

    @property
    def customer_type(self) -> CustomerType:
        return self._customer_type

    @property
    def customer_discount(self) -> float | None:
        return self._customer_discount

    @property
    def favorite_items(self) -> list[OrderItem]:
        return list[OrderItem](self._favorite_items)

    def is_vip(self) -> bool:
        return self._customer_type is CustomerType.VIP

    def add_favorite_item(self, item: OrderItem) -> None:
        """Add an item if no item with the same name is already present."""
        if not self._has_favorite_named(item.name):
            self._favorite_items.append(item)

    def remove_favorite_item(self, item: OrderItem) -> None:
        """Remove a favorite item by matching name."""
        self._favorite_items = [
            fav for fav in self._favorite_items if fav.name != item.name
        ]

    def _has_favorite_named(self, name: str) -> bool:
        return any(fav.name == name for fav in self._favorite_items)

    def take_gift(self, gift: Gift) -> None:
        self._gift = gift

    def open_gift(self) -> None:
        if self._gift is None:
            print("You have no gift to open.")
            return
        self._gift.open_gift()

    def __repr__(self) -> str:
        return (
            f"Customer(id={self._id}, name={self._first_name} {self._last_name}, "
            f"type={self._customer_type.value})"
        )