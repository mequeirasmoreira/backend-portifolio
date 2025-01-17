from pydantic import BaseModel, EmailStr

class EmailMessage(BaseModel):
    name: str
    email: EmailStr
    message: str
