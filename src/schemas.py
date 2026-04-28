from pydantic import BaseModel, ConfigDict, EmailStr


class SchemaUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class SchemaUserPublic(BaseModel):
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
