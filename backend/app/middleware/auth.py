from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.utils.auth import SECRET_KEY, ALGORITHM
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    print(f"DEBUG: Validating token: {token[:10]}...")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        print(f"DEBUG: Token payload email: {email}")
        if email is None:
            print("DEBUG: Email not found in payload")
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError as e:
        print(f"DEBUG: JWT Validation error: {str(e)}")
        raise credentials_exception
        
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email=token_data.email)
    if user is None:
        print(f"DEBUG: User not found in DB: {token_data.email}")
        raise credentials_exception
    print(f"DEBUG: User validated: {user.email}")
    return user
