from datetime import datetime, timedelta

from sqlalchemy import select, and_, extract, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate
from typing import List, Optional, Any, Coroutine, Sequence


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(self, skip: int = 0, limit: int = 100) -> Sequence[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact(self, contact_id: int) -> Optional[Contact]:
        stmt = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_contact(self, contact_data: ContactCreate) -> Contact:
        new_contact = Contact(**contact_data.dict())
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        contact = await self.get_contact(contact_id)
        if contact:
            for key, value in contact_data.dict(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        contact = await self.get_contact(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def search_contacts(self, first_name: Optional[str], last_name: Optional[str], email: Optional[str]):
        stmt = select(Contact)
        if first_name:
            stmt = stmt.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            stmt = stmt.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contacts_birthday_soon(self):
        today = datetime.today()
        seven_days_later = today + timedelta(days=7)

        stmt = select(Contact).filter(
            or_(
                and_(
                    extract('month', Contact.birthday) == today.month,
                    extract('day', Contact.birthday) >= today.day
                ),
                and_(
                    extract('month', Contact.birthday) == seven_days_later.month,
                    extract('day', Contact.birthday) <= seven_days_later.day
                )
            )
        )

        result = await self.db.execute(stmt)
        contacts = result.scalars().all()

        if contacts is None:  # Додаємо перевірку
            return []

        return contacts  # Гарантовано повертає список