from fastapi import APIRouter, Path, Response, status

from app.api.response_docs import USER_CREATE_RESPONSES, USER_DELETE_RESPONSES, USER_GET_RESPONSES
from app.core.user_store import user_store
from app.models.model_user_create_request import UserCreateRequest
from app.models.model_user_response import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    description="Создаёт пользователя из JSON payload. Логин и пароль не передаются через query string.",
    responses=USER_CREATE_RESPONSES,
)
def create_user(payload: UserCreateRequest) -> UserResponse:
    return UserResponse(**user_store.create_user(payload))


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить пользователя по идентификатору",
    responses=USER_GET_RESPONSES,
)
def get_user(user_id: int = Path(gt=0, description="Положительный идентификатор пользователя.")) -> UserResponse:
    return UserResponse(**user_store.get_user(user_id))


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя по идентификатору",
    responses=USER_DELETE_RESPONSES,
)
def delete_user(user_id: int = Path(gt=0, description="Положительный идентификатор пользователя.")) -> Response:
    user_store.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
