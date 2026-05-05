from fastapi import APIRouter, Depends, Response, status


from app.api.response_docs import AUTH_LOGIN_RESPONSES, AUTH_LOGOUT_RESPONSES, AUTH_ME_RESPONSES
from app.core.dependencies import get_authorization_token, get_current_user
from app.core.user_store import user_store
from app.models.model_auth_login_request import AuthLoginRequest
from app.models.model_auth_token_response import AuthTokenResponse
from app.models.model_user_response import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=AuthTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Выполнить вход",
    description="Принимает логин и пароль только в JSON-теле запроса, а не в query string.",
    responses=AUTH_LOGIN_RESPONSES,
)
def login(payload: AuthLoginRequest) -> AuthTokenResponse:
    token = user_store.authenticate(payload)
    return AuthTokenResponse(access_token=token)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить текущего пользователя",
    responses=AUTH_ME_RESPONSES,
)
def get_me(current_user: dict = Depends(get_current_user)) -> UserResponse:
    return UserResponse(**current_user)


@router.delete(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Завершить текущую сессию",
    responses=AUTH_LOGOUT_RESPONSES,
)
def logout(token: str = Depends(get_authorization_token)) -> Response:
    user_store.logout(token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
