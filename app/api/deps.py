from typing import Annotated

from fastapi import Depends
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer

auth = HTTPBearer()
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(auth)]
