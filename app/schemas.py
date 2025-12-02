from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str

class TodoOut(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True
