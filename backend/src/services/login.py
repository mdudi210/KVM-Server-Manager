import os
from datetime import timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi_jwt_auth import AuthJWT
from mysql.connector import Error as MySQLError

from backend.config import JWT_auth_setting
from backend.config.logging_setting import setup_logger
from backend.src.schema.schema import LoginRequest
from backend.src.utils.auth_ad import authenticate_with_ad
from backend.src.utils.db_connection import OpenDb
from backend.src.utils.hash_password import verify_password

load_dotenv()

router = APIRouter()
logger = setup_logger("login_endpoint")
RETURN_TOKEN_IN_BODY = os.getenv("RETURN_TOKEN_IN_BODY", "true").lower() in {"1", "true", "yes"}
AD_UPN_SUFFIX = os.getenv("AD_UPN_SUFFIX", "").strip()
AD_BASE_DN = os.getenv("AD_BASE_DN", "").strip()


def _derive_upn_suffix() -> str:
    if AD_UPN_SUFFIX:
        return AD_UPN_SUFFIX

    parts = []
    for token in AD_BASE_DN.split(","):
        token = token.strip()
        if token.upper().startswith("DC="):
            dc = token.split("=", 1)[1].strip()
            if dc:
                parts.append(dc)
    return ".".join(parts)


def _ad_username_candidates(username: str) -> list[str]:
    raw = username.strip()
    candidates: list[str] = []

    def _push(value: str):
        value = value.strip()
        if value and value not in candidates:
            candidates.append(value)

    _push(raw)

    # DOMAIN\user -> user
    if "\\" in raw:
        _push(raw.split("\\")[-1])

    # user@domain -> user
    if "@" in raw:
        _push(raw.split("@", 1)[0])

    suffix = _derive_upn_suffix()
    base = raw.split("\\")[-1].split("@", 1)[0]
    if suffix and "@" not in raw:
        _push(f"{base}@{suffix}")

    return candidates


def _db_username_candidates(username: str) -> list[str]:
    raw = username.strip()
    candidates: list[str] = []

    def _push(value: str):
        value = value.strip()
        if value and value not in candidates:
            candidates.append(value)

    _push(raw)
    if "\\" in raw:
        _push(raw.split("\\")[-1])
    if "@" in raw:
        _push(raw.split("@", 1)[0])
    return candidates


def _authenticate_local_exact(username: str, password: str) -> tuple[str, str, str]:
    with OpenDb() as cursor:
        cursor.execute(
            """
            SELECT u.id, u.username, u.password, r.role
            FROM users u
            JOIN roles r ON r.id = u.role_id
            WHERE u.username = %s
            """,
            (username,),
        )
        result = cursor.fetchone()

    if not result or not verify_password(password, result[2]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return result[0], result[1], result[3]


def _authenticate_local_with_fallback_candidates(username: str, password: str) -> tuple[str, str, str]:
    last_error: HTTPException | None = None
    for candidate in _db_username_candidates(username):
        try:
            return _authenticate_local_exact(candidate, password)
        except HTTPException as exc:
            last_error = exc
    if last_error:
        raise last_error
    raise HTTPException(status_code=401, detail="Invalid username or password")


def _authenticate_ad_first_then_db(username: str, password: str) -> tuple[str, str, str, str]:
    ad_error: HTTPException | None = None

    for candidate in _ad_username_candidates(username):
        try:
            result = authenticate_with_ad(candidate, password)
            if not result[0]:
                continue
            return result[2], candidate, result[1], "ad"
        except HTTPException as exc:
            # Invalid AD role should remain a hard deny.
            if exc.status_code == 403:
                raise
            ad_error = exc

    # AD not reachable / AD user missing / invalid AD auth -> try DB.
    try:
        user_id, db_username, role = _authenticate_local_with_fallback_candidates(username, password)
        return user_id, db_username, role, "local"
    except HTTPException:
        if ad_error:
            raise ad_error
        raise


def _build_login_response(
    *,
    response: Response,
    authorize: AuthJWT,
    user_id: str,
    username: str,
    role: str,
    auth_provider: str,
) -> dict:
    access_token = authorize.create_access_token(
        subject=username,
        expires_time=timedelta(days=7),
        user_claims={"id": user_id, "role": role},
    )

    authorize.set_access_cookies(access_token, response)

    payload = {
        "id": user_id,
        "username": username,
        "role": role,
        "auth_provider": auth_provider,
    }

    if RETURN_TOKEN_IN_BODY:
        payload["access_token"] = access_token

    return payload


@router.post("/login")
def login(data: LoginRequest, response: Response, Authorize: AuthJWT = Depends()):
    try:
        user_id, username, role, provider = _authenticate_ad_first_then_db(data.username, data.password)

        logger.info("User '%s' logged in successfully via %s", username, provider)
        return _build_login_response(
            response=response,
            authorize=Authorize,
            user_id=user_id,
            username=username,
            role=role,
            auth_provider=provider,
        )

    except HTTPException:
        raise
    except MySQLError:
        logger.exception("Database error occurred during login")
        raise HTTPException(status_code=500, detail="Database error")
    except Exception:
        logger.exception("Unexpected error in login API")
        raise HTTPException(status_code=500, detail="Unexpected error in login API")


@router.post("/logout")
def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies(response)
    return {"message": "Logged out successfully"}
