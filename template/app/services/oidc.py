import logging
import time
from typing import Any

import httpx
import jwt
from jwt import PyJWKClient

from app.core.config import settings

logger = logging.getLogger(__name__)


class OIDCProvider:
    """Dynamically fetches OIDC metadata and handles identity verification."""

    def __init__(self, authority: str, client_id: str, cache_ttl_seconds: int = 3600):
        # authority (or issuer) is the base URL of the Identity Provider
        self.authority = authority.rstrip("/")
        self.client_id = client_id
        self.well_known_url = f"{self.authority}/.well-known/openid-configuration"
        self.cache_ttl_seconds = cache_ttl_seconds

        self._config: dict[str, Any] = {}
        self.jwks_client: PyJWKClient | None = None

        # Encapsulate the role cache inside the instance
        self._role_cache: dict[str, dict[str, Any]] = {}

        # Synchronously load config so Swagger UI gets the URLs at startup
        self._load_config()

    def _load_config(self) -> None:
        """Fetches the OIDC discovery document and initializes the JWKS client."""
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.well_known_url)
                response.raise_for_status()
                self._config = response.json()

            jwks_uri = self._config.get("jwks_uri")
            if not jwks_uri:
                raise ValueError("OIDC metadata missing 'jwks_uri'")

            # JWKS Client with automated key caching and rotation handling
            self.jwks_client = PyJWKClient(jwks_uri, cache_keys=True)
            logger.info(
                f"✅ OIDC Provider configured securely via: {self.well_known_url}"
            )

        except Exception as e:
            logger.error(
                f"🚨 Failed to fetch OIDC metadata from {self.well_known_url}: {e}"
            )
            raise RuntimeError(f"Could not initialize OIDC Provider: {e}") from e

    @property
    def auth_url(self) -> str:
        return self._config.get("authorization_endpoint", "")

    @property
    def token_url(self) -> str:
        return self._config.get("token_endpoint", "")

    @property
    def userinfo_url(self) -> str:
        return self._config.get("userinfo_endpoint", "")

    def verify_token(self, token: str) -> dict:
        """Verifies the JWT signature and audience/client_id dynamically."""
        if not self.jwks_client:
            raise RuntimeError("OIDC Provider not initialized")

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                # We disable standard audience verification to manually support
                # enterprise environments that use `client_id` or `azp` instead.
                options={"verify_aud": False},
            )

            # Agnostic check for client_id or azp depending on the IdP's token structure
            token_client_id = (
                payload.get("client_id") or payload.get("azp") or payload.get("aud")
            )

            # If aud is a list, check if client_id is in it
            if isinstance(token_client_id, list):
                if self.client_id not in token_client_id:
                    raise jwt.InvalidTokenError(
                        "Token audience list does not contain our client_id."
                    )
            elif token_client_id != self.client_id:
                raise jwt.InvalidTokenError(
                    f"Token client_id/azp '{token_client_id}' does not match '{self.client_id}'."
                )

            return payload

        except jwt.PyJWTError as e:
            logger.error(f"🚨 Security Rejection - Invalid Token: {e!s}")
            raise e

    async def get_user_roles(self, access_token: str, uid: str) -> list[str]:
        """Fetches roles from instance cache, or falls back to UserInfo endpoint."""
        current_time = time.time()

        # 1. Check encapsulated cache
        if uid in self._role_cache:
            cached = self._role_cache[uid]
            if current_time < cached["expires_at"]:
                return cached["roles"]

        if not self.userinfo_url:
            logger.warning("No UserInfo endpoint discovered. Returning empty roles.")
            return []

        # 2. Fetch from Identity Provider
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.userinfo_url,
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=5.0,
                )
                response.raise_for_status()
                user_data = response.json()

            # 3. Agnostic role extraction (handles Okta, Keycloak, Azure AD, Ping)
            roles = user_data.get(
                "role", user_data.get("roles", user_data.get("groups", []))
            )
            if isinstance(roles, str):
                roles = [roles]

            # 4. Update instance cache
            self._role_cache[uid] = {
                "roles": roles,
                "expires_at": current_time + self.cache_ttl_seconds,
            }
            return roles

        except Exception as e:
            logger.error(f"Failed to fetch UserInfo from {self.userinfo_url}: {e}")
            return []


# Initialize singleton for dependency injection
oidc_provider = OIDCProvider(
    authority=settings.oidc_authority,
    client_id=settings.oidc_client_id,
)
