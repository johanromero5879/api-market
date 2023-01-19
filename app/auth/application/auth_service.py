from app.common.application import Service
from app.auth.domain import AuthRepository, Token, TokenData
from app.auth.application import CredentialsError
from app.common.application import JWTService, BCryptService


class AuthService(Service):
    _repository: AuthRepository
    __jwt_service: JWTService
    __bcrypt_service: BCryptService

    def __init__(self, repository: AuthRepository):
        super().__init__(repository)
        self.__jwt_service = JWTService()
        self.__bcrypt_service = BCryptService()

    def authenticate_user(self, email: str, password: str) -> Token:
        user_found = self._repository.find_by("email", email)

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
