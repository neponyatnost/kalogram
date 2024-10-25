from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True