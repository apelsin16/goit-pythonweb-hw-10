from datetime import date
from typing import Optional

from sqlalchemy import String, Date, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    birthday: Mapped[date] = mapped_column(Date)
    extra_info: Mapped[Optional[str]] = mapped_column(String, nullable=True)
