from select import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.contacts import ContactRepository
from src.schemas import ContactCreate, ContactUpdate
from src.database.models import Contact
from typing import Optional, Sequence


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repo = ContactRepository(db)
        self.db = db

    async def get_contacts(self, skip: int = 0, limit: int = 100) -> Sequence[Contact]:
        return await self.contact_repo.get_contacts(skip, limit)

    async def get_contact(self, contact_id: int) -> Optional[Contact]:
        return await self.contact_repo.get_contact(contact_id)

    async def create_contact(self, contact_data: ContactCreate) -> Contact:
        return await self.contact_repo.create_contact(contact_data)

    async def update_contact(self, contact_id: int, contact_data: ContactUpdate) -> Optional[Contact]:
        return await self.contact_repo.update_contact(contact_id, contact_data)

    async def delete_contact(self, contact_id: int) -> Optional[Contact]:
        return await self.contact_repo.delete_contact(contact_id)

    async def search_contacts(self, first_name: Optional[str], last_name: Optional[str], email: Optional[str]) -> list:
        query = select(Contact)
        if first_name:
            query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
        if last_name:
            query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
        if email:
            query = query.filter(Contact.email.ilike(f"%{email}%"))
        result = await self.db.execute(query)
        return result.scalars().all()
