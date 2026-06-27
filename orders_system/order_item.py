from orders_system.exceptions import DuplicateIdError

class OrderItem:
    """A single item inside an order. Each item has a unique id."""

    _used_ids: set[int] = set()

    def __init__(self, item_id: int, name: str, price: float) -> None:
        self._validate_id(item_id)
        self._validate_price(price)

        OrderItem._used_ids.add(item_id)
        self._id: int = item_id
        self._name: str = name
        self._price: float = price

    @staticmethod
    def _validate_id(item_id: int) -> None:
        if item_id in OrderItem._used_ids:
            raise DuplicateIdError(entity="OrderItem", entity_id=item_id)

    @staticmethod
    def _validate_price(price: float) -> None:
        if price < 0:
            raise ValueError(f"Item price cannot be negative: {price}")

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    def __repr__(self) -> str:
        return f"OrderItem(id={self._id}, name={self._name!r}, price={self._price})"