from pydantic import BaseModel

from app.common.application.service import Service
from app.auth.domain.auth_repository import AuthRepository
from app.auth.application.auth_errors import CredentialsError
from app.common.domain.value_id import ValueID
from app.common.application.jwt_service import JWTService
from app.common.application.bcrypt_service import BCryptService


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: ValueID | None = None


class AuthService(Service):
    _repository: AuthRepository
    __jwt_service: JWTService
    __bcrypt_service: BCryptService

    def __init__(self, repository: AuthRepository):
        super().__init__(repository)
        self.__jwt_service = JWTService()
        self.__bcrypt_service = BCryptService()

    def authenticate_user(self, email: str, password: str) -> Token:
        user_found = self._repository.find_by_email(email)

        if not user_found or not self.__bcrypt_service.compare(password, user_found.password):
            raise CredentialsError()

        payload = {"sub": f"user_id:{user_found.id}"}

        return Token(
            access_token=self.__jwt_service.create_access_token(payload),
            token_type="bearer"
        )

    def get_user_payload(self, token: str) -> TokenData:
        try:
            payload = self.__jwt_service.decode(token)
            if "sub" not in payload:
                raise CredentialsError()

            user_id = payload.get("sub").replace("user_id:", "")
            return TokenData(user_id=user_id)
        except Exception:
            raise CredentialsError()
