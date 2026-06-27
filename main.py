from datetime import date

from orders_system.enums import CustomerType, OrderType, PaymentType
from orders_system.exceptions import NotVipCustomerError
from orders_system.customer import Customer
from orders_system.order_item import OrderItem
from orders_system.order import Order
from orders_system.gifts import SimpleGift, NamedGift
from orders_system.bonus_animals import Spider, Cat, Fish


def demo_regular_order() -> None:
    print("=== Regular order ===")
    customer = Customer(
        customer_id=1,
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        delivery_address="1 Main St",
        customer_type=CustomerType.REGULAR,
    )
    items = [
        OrderItem(item_id=101, name="Keyboard", price=120.0),
        OrderItem(item_id=102, name="Mouse", price=80.0),
    ]
    order = Order(
        order_id=1001,
        name="Office gear",
        delivery_address="1 Main St",
        items=items,
        customer=customer,
        payment_type=PaymentType.CREDIT_CARD,
        order_type=OrderType.REGULAR,
        order_date=date(2026, 6, 27),
    )
    print(order)  # total = 200.00 (no discount)
    print("Favorites:", [i.name for i in customer.favorite_items])


def demo_vip_order() -> None:
    print("\n=== VIP order ===")
    customer = Customer(
        customer_id=2,
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        delivery_address="2 Park Ave",
        customer_type=CustomerType.VIP,
        customer_discount=15,  # 15%
    )
    items = [
        OrderItem(item_id=201, name="Laptop", price=1000.0),
        OrderItem(item_id=202, name="Headphones", price=200.0),
    ]
    order = Order(
        order_id=1002,
        name="Premium kit",
        delivery_address="2 Park Ave",
        items=items,
        customer=customer,
        payment_type=PaymentType.CASH,
        order_type=OrderType.VIP,
    )
    print(order)  # total = 1200 * 0.85 = 1020.00


def demo_vip_order_by_non_vip() -> None:
    print("\n=== VIP order by non-VIP customer (should fail) ===")
    customer = Customer(
        customer_id=3,
        first_name="Bob",
        last_name="Brown",
        email="bob@example.com",
        delivery_address="3 Oak Rd",
        customer_type=CustomerType.REGULAR,
    )
    items = [OrderItem(item_id=301, name="Watch", price=500.0)]
    try:
        Order(
            order_id=1003,
            name="Invalid VIP",
            delivery_address="3 Oak Rd",
            items=items,
            customer=customer,
            payment_type=PaymentType.CHECK,
            order_type=OrderType.VIP,
        )
    except NotVipCustomerError as exc:
        print("Caught expected error:", exc)


def demo_gifts() -> None:
    print("\n=== Gifts ===")
    customer = Customer(
        customer_id=4,
        first_name="Alice",
        last_name="Green",
        email="alice@example.com",
        delivery_address="4 Pine St",
        customer_type=CustomerType.VIP,
        customer_discount=10,
    )
    customer.open_gift()  # no gift yet
    customer.take_gift(SimpleGift())
    customer.open_gift()
    customer.take_gift(NamedGift("Coffee Mug"))
    customer.open_gift()


def demo_favorites_dedup() -> None:
    print("\n=== Favorites dedup (same name, different id) ===")
    customer = Customer(
        customer_id=5,
        first_name="Eve",
        last_name="White",
        email="eve@example.com",
        delivery_address="5 Elm St",
        customer_type=CustomerType.REGULAR,
    )
    Order(
        order_id=1005,
        name="First",
        delivery_address="5 Elm St",
        items=[OrderItem(item_id=501, name="Book", price=30.0)],
        customer=customer,
        payment_type=PaymentType.OTHER,
        order_type=OrderType.REGULAR,
    )
    # Same name "Book", different id -> should NOT be added again.
    Order(
        order_id=1006,
        name="Second",
        delivery_address="5 Elm St",
        items=[OrderItem(item_id=502, name="Book", price=30.0)],
        customer=customer,
        payment_type=PaymentType.OTHER,
        order_type=OrderType.REGULAR,
    )
    print("Favorites:", [i.name for i in customer.favorite_items])  # ['Book'] once


def demo_bonus_animals() -> None:
    print("\n=== Bonus: animals ===")
    spider = Spider()
    spider.walk()
    spider.eat()

    cat = Cat("Whiskers")
    cat.walk()
    cat.play()
    cat.eat()
    print("Cat name:", cat.get_name())

    fish = Fish("Nemo")
    fish.walk()  # overridden
    fish.play()
    fish.eat()


def main() -> None:
    demo_regular_order()
    demo_vip_order()
    demo_vip_order_by_non_vip()
    demo_gifts()
    demo_favorites_dedup()
    demo_bonus_animals()


if __name__ == "__main__":
    main()
