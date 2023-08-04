"""Customer data model.

Here we implement our data model for customers, a dataclass with
fields firstname, lastname, customer_id (a hash).
"""
import sys
from dataclasses import dataclass, field


@dataclass(frozen=False)  # frozen means that the object cannot be modified after creation!
class Customer:
    """A class representing one single customer."""

    firstname: str = ""
    lastname: str = ""
    id_: int = field(default=-1024, init=False)

    def __post_init__(self):
        self.__hash__()

    @property
    def fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"

    def __eq__(self, other: "Customer") -> bool:
        if isinstance(other, type(self)):
            return all([
                getattr(self, attr) == getattr(other, attr)
                for attr in ["firstname", "lastname"]])
        else:
            raise TypeError("Cannot compare different types")

    def __lt__(self, other: "Customer"):
        try:
            assert len({type(x) for x in [self, other]}) == 1

            if not hasattr(self, "fullname"):
                setattr(self, 'fullname', f'{self.firstname}{self.lastname}')

            if not hasattr(other, 'fullname'):
                setattr(other, 'fullname', f'{other.firstname}{other.lastname}')

            return self.fullname < other.fullname

        except AssertionError as e:
            print('Error:', e)

    def __repr__(self):
        return f"Customer('{self.firstname}', '{self.lastname}','{hex(abs(self.id_))[-6:]})"

    def __hash__(self):
        hsh = abs(hash((self.firstname + self.lastname))) % ((sys.maxsize + 1) * 2) + sys.maxsize * 3
        self.id_ = hsh

        return hsh


if __name__ == "__main__":
    # added manually
    customer = Customer("Ben", "Auffarth")
    customer2 = Customer("Paul", "Smith")
    print(customer == customer2)
