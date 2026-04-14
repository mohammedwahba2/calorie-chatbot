from pydantic import BaseModel, Field


class UserInput(BaseModel):
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
    age: int = Field(gt=0)
    gender: str = "male"
    activity_level: float = Field(gt=0)
    goal: str
