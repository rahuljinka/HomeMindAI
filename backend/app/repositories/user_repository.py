from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.auth import get_password_hash
from app.models.memory import House

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
        
        # Create Main House
        main_house = House(user_id=db_user.id, name="Main House")
        self.db.add(main_house)
        await self.db.commit()
        
        return db_user
