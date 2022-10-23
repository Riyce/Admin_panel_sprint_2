from datetime import datetime

from pydantic import BaseModel


class CreeateMixin(BaseModel):
    @classmethod
    def get_object(cls, base_obj: BaseModel, user_id: str):
        payload = base_obj.dict()
        payload["user_id"] = user_id
        if "time" in cls.__fields__ and cls.__fields__["time"].type_ == datetime:
            payload["time"] = datetime.now().replace(microsecond=0)
        return cls(**payload)
