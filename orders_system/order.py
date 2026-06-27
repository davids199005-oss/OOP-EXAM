from datetime import date

from orders_system.enums import OrderType, PaymentType
from orders_system.customer import Customer
from orders_system.order_item import OrderItem
from orders_system.exceptions import DuplicateIdError, NotVipCustomerError


class Order:
    """A customer order. Each order has a unique id.

    Total price is calculated in the constructor as the sum of item prices.
    For a VIP order, the customer's discount is applied; a VIP order made by
    a non-VIP customer raises NotVipCustomerError.
    """

    _used_ids: set[int] = set[int]()

    def __init__(
        self,
        order_id: int,
        name: str,
        delivery_address: str,
        items: list[OrderItem],
        customer: Customer,
        payment_type: PaymentType,
        order_type: OrderType,
        order_date: date | None = None,
    ) -> None:
        self._validate_id(order_id)

        Order._used_ids.add(order_id)
        self._id: int = order_id
        self._name: str = name
        self._delivery_address: str = delivery_address
        self._items: list[OrderItem] = list[OrderItem](items)
        self._customer: Customer = customer
        self._payment_type: PaymentType = payment_type
        self._order_type: OrderType = order_type
        self._order_date: date = order_date if order_date is not None else date.today()

        self._total_price: float = self._calculate_total_price()
        self._add_items_to_customer_favorites()

    @staticmethod
    def _validate_id(order_id: int) -> None:
        if order_id in Order._used_ids:
            raise DuplicateIdError(entity="Order", entity_id=order_id)

    def _calculate_total_price(self) -> float:
        base_total = sum(item.price for item in self._items)

        if self._order_type is OrderType.REGULAR:
            return base_total

        if not self._customer.is_vip():
            raise NotVipCustomerError(customer_id=self._customer.id)

        discount = self._customer.customer_discount or 0
        return base_total * (1 - discount / 100)

    def _add_items_to_customer_favorites(self) -> None:
        for item in self._items:
            self._customer.add_favorite_item(item)

    @property
    def id(self) -> int:
        return self._id

    @property
    def items(self) -> list[OrderItem]:
        return list[OrderItem](self._items)

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def total_price(self) -> float:
        return self._total_price

    @property
    def order_type(self) -> OrderType:
        return self._order_type

    def __repr__(self) -> str:
        return (
            f"Order(id={self._id}, type={self._order_type.value}, "
            f"total={self._total_price:.2f})"
        )
