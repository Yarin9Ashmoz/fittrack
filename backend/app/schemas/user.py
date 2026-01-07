from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str = Field(..., pattern=r"^05\d{8}$")
    address: str | None = None
    role: str = Field(..., pattern="^(member|coach|admin)$")
    status: str = "active"


class UserUpdateSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(None, pattern=r"^05\d{8}$")
    address: str | None = None
    role: str | None = Field(None, pattern="^(member|coach|admin)$")
    status: str | None = None


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str | None
    role: str
    status: str

    model_config = {"from_attributes": True}
