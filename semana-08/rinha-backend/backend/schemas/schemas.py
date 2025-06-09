from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int = Field(default=None, gt=0)
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str = Field(max_length=100)
    email: str = Field(max_length=100)
    password: str


class TransactionSchema(BaseModel):
    id: int = Field(default=None, gt=0)
    amount: float
    timestamp: str
    status: str

    class Config:
        orm_mode = True


class TransactionCreate(BaseModel):
    amount: float
    timestamp: str
    status: str = "pending"
    user: int  
