from dataclasses import dataclass


@dataclass
class Genre:
    g_id:       str = None
    genre_name: str = None

    def to_dict(self):
        return dict(id=self.g_id, name=self.genre_name)

    @property
    def id(self):
        return self.g_id
