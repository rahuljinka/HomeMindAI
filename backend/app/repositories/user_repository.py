from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.utils.auth import get_password_hash

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def create_user(self, user: UserCreate):
        db_user = User(
            email=user.email,
            password_hash=get_password_hash(user.password)
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
