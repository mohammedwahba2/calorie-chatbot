from pydantic import BaseModel

class User(BaseModel):
    weight: float
    height: float
    age: int
    gender: str
    activity_level: float
    goal: str