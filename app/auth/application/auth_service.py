from pydantic import BaseModel

from app.common.application.service import Service
from app.auth.domain.auth_repository import AuthRepository
from app.auth.domain.auth import Auth
from app.auth.application.auth_errors import CredentialsError
from app.common.application.jwt_service import JWTService
from app.common.application.bcrypt_service import BCryptService


class AuthResponse(BaseModel):
    access_token: str
    token_type: str


class AuthService(Service):
    _repository: AuthRepository
    __jwt_service: JWTService
    __bcrypt_service: BCryptService

    def __init__(self, repository: AuthRepository):
        super().__init__(repository)
        self.__jwt_service = JWTService()
        self.__bcrypt_service = BCryptService()

    def get_auth(self, user: Auth) -> AuthResponse:
        user_found = self._repository.find_by_email(user.email)

        if not user_found or not self.__bcrypt_service.compare(user.password, user_found.password):
            raise CredentialsError()

        payload = {
            "sub": user_found.id,
            "name": f"{user_found.first_name} {user_found.last_name}",
            "email": user.email
        }

        return AuthResponse(
            access_token=self.__jwt_service.encrypt(payload),
            token_type="bearer"
        )
