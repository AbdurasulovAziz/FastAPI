from sqlalchemy.ext.asyncio import AsyncSession
from app.account.models import User
from app.account.services import UserService
from app.auth.schema import UserLoginSchema, UserRegistrationSchema
from app.auth.views import check_authentication_data, hash_password


class AuthService:
    def __init__(
        self, auth_data: UserLoginSchema | UserRegistrationSchema, db: AsyncSession
    ):
        self.data = auth_data.dict()
        self.db = db

    async def authenticate_user(self):
        user = await UserService(self.data, self.db).get_current_user()

        token = check_authentication_data(user, self.data.get("password"))

        return {"token": token}

    async def registrate_user(self):
        new_user = User(**self.data)
        password = hash_password(new_user.password)

        new_user.password = password

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user
