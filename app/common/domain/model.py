from bson import ObjectId
from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
