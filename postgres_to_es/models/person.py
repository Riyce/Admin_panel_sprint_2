from dataclasses import dataclass
from typing import List


@dataclass
class Person:
    p_id: str = None
    name: str = None

    def to_dict(self):
        return dict(id=self.p_id, name=self.name)


@dataclass
class PersonFull:
    id: str = None
    full_name: str = None
    roles: List[str] = None
    film_ids: List[str] = None

    def to_dict(self):
        return dict(id=self.id, full_name=self.full_name, roles=self.roles, film_ids=self.film_ids)
