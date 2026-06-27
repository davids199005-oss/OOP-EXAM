from orders_system.interfaces import Gift


class SimpleGift(Gift):

    _CONGRATS_MESSAGE = "Congratulations! you got a new gift! Enjoy!"

    def open_gift(self) -> None:
        print(SimpleGift._CONGRATS_MESSAGE)


class NamedGift(Gift):
    """A gift that also carries a description (e.g. 'Coffee Mug')."""

    _CONGRATS_MESSAGE = "Congratulations! you got a new gift! Enjoy!"

    def __init__(self, description: str) -> None:
        self._description: str = description

    @property
    def description(self) -> str:
        return self._description

    def open_gift(self) -> None:
        print(NamedGift._CONGRATS_MESSAGE)
        print(f"Your gift: {self._description}")
