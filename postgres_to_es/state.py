import abc
import json
from typing import Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):

    def __init__(self, file_path: str = None) -> None:
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(state, file, ensure_ascii=False)
        return None

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as file:
                state_dict = json.load(file)
        except FileNotFoundError:
            state_dict = {}
        return state_dict


class State:
    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        data = self.storage.retrieve_state()
        data[key] = value
        self.storage.save_state(data)

    def get_state(self, key: str) -> Any:
        data = self.storage.retrieve_state()
        result = data.get(key)
        return result
