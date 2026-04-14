from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=4)
    message: str = Field(min_length=1)


class ChatResponse(BaseModel):
    reply: str
    language: str
    missing_fields: list[str]
    profile: dict


class ProfileResponse(BaseModel):
    email: str
    profile: dict


class MealLogRequest(BaseModel):
    meal_type: str = Field(pattern="^(breakfast|lunch|dinner|snack)$")
    description: str = Field(min_length=2)
    calories: float | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None
    session_id: str | None = None


class MealResponse(BaseModel):
    id: int
    meal_type: str
    description: str
    calories: float | None
    protein_g: float | None
    carbs_g: float | None
    fat_g: float | None
    logged_at: str


class ProgressLogRequest(BaseModel):
    weight: float = Field(gt=0)
    note: str | None = None


class ProgressResponse(BaseModel):
    id: int
    weight: float
    note: str | None
    logged_at: str
