from app.common.domain import ValueId
from app.user.application import UserFoundError
from app.auth.domain import AuthRepository, TokenData, AuthIn, BaseAuth
from app.auth.application import CredentialsError
from app.common.application import JWTService, BCryptService, Service


class AuthService(Service):
    __repository: AuthRepository
    __jwt_service: JWTService
    __bcrypt_service: BCryptService

    def __init__(self,
                 repository: AuthRepository,
                 jwt_service: JWTService,
                 bcrypt_service: BCryptService
                 ):
        self.__repository = repository
        self.__jwt_service = jwt_service
        self.__bcrypt_service = bcrypt_service

    def exists_by(self, field: str, value):
        return self.__repository.exists_by(field, value)

    def authenticate_user(self, email: str, password: str) -> ValueId:
        user_found = self.__repository.find_by("email", email)

        if not user_found or not self.__bcrypt_service.compare(password, user_found.password):
            raise CredentialsError()

        return user_found.id

    def register_user(self, user: BaseAuth) -> ValueId:
        # Transform to UserIn instances to set default attributes before create them
        user = AuthIn(**user.dict())

        # By default, users get $500 to try out the app
        user.budget = 500

        if self.__repository.exists_by("email", user.email):
            raise UserFoundError(email=user.email)

        user.password = self.__bcrypt_service.create_hash(user.password)

        user_id = self.__repository.insert_one(user)

        return user_id

    def generate_user_tokens(self, id: ValueId) -> tuple[str, str]:
        """
        :param id: user id
        :return: access token and refresh token
        """

        identifier = f"user_id:{id}"
        access_token = self.__jwt_service.create_access_token(identifier)
        refresh_token = self.__jwt_service.create_refresh_token(identifier)

        return access_token, refresh_token

    def get_user_payload(self, token: str) -> TokenData:
        try:
            payload = self.__jwt_service.decode(token)
            if "sub" not in payload:
                raise CredentialsError()

            user_id = payload.get("sub").replace("user_id:", "")
            return TokenData(user_id=user_id)
        except Exception:
            raise CredentialsError()
