from typing import Any

from aiohttp.client import ClientSession
from fastapi import Depends, status
from fastapi.exceptions import HTTPException

from core.config import USER_CHECK_URL
from models.credentials import HTTPAuthorizationCredentials
from utils.depends import HTTPBearer


oauth2_scheme = HTTPBearer()


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    user = await AuthService.validate_token(token)
    return user


class AuthService:
    @classmethod
    async def validate_token(cls, token: HTTPAuthorizationCredentials) -> Any:
        headers = {"Authorization": f"Bearer {token.credentials}", "user-agent": token.agent}
        async with ClientSession(headers=headers) as session:
            async with session.get(USER_CHECK_URL) as r:
                json_body = await r.json()
                if r.status == status.HTTP_200_OK:
                    return json_body
                elif r.status == status.HTTP_403_FORBIDDEN:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail=json_body['message']
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=json_body
                    )
