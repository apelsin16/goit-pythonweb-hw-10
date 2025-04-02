from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

# Схема для створення нового контакту (Create Contact)
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: datetime
    extra_info: Optional[str] = None

    class Config:
        # Це допомагає використовувати SQLAlchemy моделі для Pydantic
        orm_mode = True

# Схема для читання даних про контакт (Read Contact)
class ContactRead(ContactCreate):
    id: int

    class Config:
        orm_mode = True

# Схема для оновлення контакту (Update Contact)
class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birthday: Optional[date]
    extra_info: Optional[str] = None

    class Config:
        orm_mode = True
