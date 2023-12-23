from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User, UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        query = select(self.model).where(self.model.email == email)
        result = await session.exec(query)
        return result.first()

    async def create(
        self, session: AsyncSession, obj_in: UserCreate, is_superuser: bool = False
    ) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=is_superuser,
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, db_obj: User, obj_in: UserUpdate
    ) -> User:
        obj_data = obj_in.model_dump(exclude_unset=True)
        if password := obj_data.get("password"):
            hashed_password = get_password_hash(password)
            del obj_data["password"]
            obj_data["hashed_password"] = hashed_password
        return await super().update(session, db_obj=db_obj, obj_in=obj_data)

    async def authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> User | None:
        user = await self.get_by_email(session, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def activate(self, session: AsyncSession, db_obj: User) -> bool:
        db_obj.is_active = True
        session.add(db_obj)
        await session.commit()
        return True


crud_user = CRUDUser(User)
