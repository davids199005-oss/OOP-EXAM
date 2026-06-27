class DuplicateIdError(Exception):
    """Raised when an entity is created with an already-used id."""

    def __init__(self, entity: str, entity_id: int) -> None:
        super().__init__(f"{entity} with id={entity_id} already exists.")
        self.entity: str = entity
        self.entity_id: int = entity_id


class NotVipCustomerError(Exception):
    """Raised when a VIP order is made by a non-VIP customer."""

    def __init__(self, customer_id: int) -> None:
        super().__init__(
            f"Customer id={customer_id} is not a VIP customer "
            f"but a VIP order was requested."
        )
        self.customer_id: int = customer_id