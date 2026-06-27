from abc import ABC, abstractmethod


class Pet(ABC):
    """Interface for animals that can be kept as pets."""

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def set_name(self, name: str) -> None: ...

    @abstractmethod
    def play(self) -> None: ...


class Animal(ABC):
    """Abstract base animal. Has a number of legs, can walk, and must eat."""

    def __init__(self, legs: int) -> None:
        self._legs: int = legs

    @property
    def legs(self) -> int:
        return self._legs

    def walk(self) -> None:
        print(f"Walking on {self._legs} legs.")

    @abstractmethod
    def eat(self) -> None: ...


class Spider(Animal):
    """A spider: an animal with 8 legs, but not a pet."""

    _DEFAULT_LEGS = 8

    def __init__(self) -> None:
        super().__init__(legs=Spider._DEFAULT_LEGS)

    def eat(self) -> None:
        print("The spider catches insects in its web.")


class Cat(Animal, Pet):
    """A cat: a four-legged animal that is also a pet."""

    _DEFAULT_LEGS = 4

    def __init__(self, name: str = "") -> None:
        super().__init__(legs=Cat._DEFAULT_LEGS)
        self._name: str = name

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def play(self) -> None:
        print(f"{self._name or 'The cat'} plays with a ball of yarn.")

    def eat(self) -> None:
        print("The cat eats fish and meat.")


class Fish(Animal, Pet):
    """A fish: a pet animal with no legs that swims instead of walking."""

    _DEFAULT_LEGS = 0

    def __init__(self, name: str = "") -> None:
        super().__init__(legs=Fish._DEFAULT_LEGS)
        self._name: str = name

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def play(self) -> None:
        print(f"{self._name or 'The fish'} blows bubbles.")

    def walk(self) -> None:
        print("Fish can't walk - it swims instead.")

    def eat(self) -> None:
        print("The fish eats algae and fish flakes.")
