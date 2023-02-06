"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from __future__ import annotations

import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from typing import TYPE_CHECKING, Literal

from django.conf import settings
from rest_framework.exceptions import ValidationError

if TYPE_CHECKING:
    from apps.users.models import User


def encode_to_b64(data: bytes) -> str:
    """Encode data to base64. The data is encoded using the URL-safe
    base64 encoding scheme and the padding is removed.

    Parameters
    ----------
    data: :class:`bytes`
        The data to encode.

    Returns
    -------
    :class:`str`
        The encoded data.
    """
    return urlsafe_b64encode(data).decode("utf-8").strip("=")


def decode_from_b64(data: str) -> bytes:
    """Decode data from base64. The data is decoded using the URL-safe
    base64 encoding scheme and the padding is added.

    Parameters
    ----------
    data: :class:`str`
        The data to decode.

    Returns
    -------
    :class:`str`
        The decoded data.
    """
    return urlsafe_b64decode(data + "==")


def _generate_token_v1(
    user_id: str, email: str, password: str
) -> tuple[str, str]:
    signature = f"{email}.{password}".encode("utf-8")
    message = encode_to_b64(signature).encode("utf-8")

    key = settings.SECRET_KEY.encode("utf-8")

    hmac_component = encode_to_b64(hmac.new(key, message, "sha256").digest())
    id_part = encode_to_b64(user_id.encode("utf-8"))

    return (id_part, hmac_component)


Version = Literal["v1"]


def generate_token(
    user_id: str, email: str, password: str, version: Version = "v1"
) -> str:
    """Generate a unique token for the user. The first part of the token
    is the version of the token so that the application can handle
    different versions of the token. The second part of the token is the
    ID of the user so that the user can be identified. The third part of
    the token is a HMAC component which is used to verify the
    authenticity of the token. The HMAC component is generated using the
    user's email, password and the server's secret key, the component is
    generated using the SHA256 hashing algorithm and the token is
    generated using the following format:


    Version: v1
    +---------+------------------+--------------------------------+
    | Version |   ID (base64)    |          HMAC (base64)         |
    +---------+------------------+--------------------------------+
    |   v1    |   MTIzNDU2Nzg5   | NGzHnCFb2A9PTG4BHRAHMr4EfbKoCW |
    +---------+------------------+--------------------------------+

    Parameters
    ----------
    user_id: :class:`str`
        The ID of the user.
    email: :class:`str`
        The e-mail of the user.
    password: :class:`str`
        The password of the user.

    Returns
    -------
    :class:`str`
        A unique token for the user.
    """
    match version:
        case "v1":
            token = _generate_token_v1(user_id, email, password)

    return ".".join([version, *token])


def _validate_token_v1(id_part: str, hmac_component: str) -> tuple[User, str]:
    # to avoid circular imports
    from apps.users.models import User

    try:
        user_id = decode_from_b64(id_part).decode("utf-8")
        user = User.objects.get(id=user_id)
    except (UnicodeDecodeError, User.DoesNotExist) as exc:
        raise ValidationError("Invalid token.") from exc

    _, expected = _generate_token_v1(user_id, user.email, user.password)

    try:
        decoded_expected = decode_from_b64(expected)
        decoded_hmac_component = decode_from_b64(hmac_component)
    except (UnicodeDecodeError, BinasciiError) as exc:
        raise ValidationError("Invalid token.") from exc

    if not hmac.compare_digest(decoded_hmac_component, decoded_expected):
        raise ValidationError("Invalid token.")

    return (user, user.token)


def validate_token(token: str) -> tuple[User, str]:
    """Validate the token. The token is validated using the following
    steps:

    1. The token is split into its parts.
    2. The version of the token is checked.
    3. The token is validated using the version of the token.

    Parameters
    ----------
    token: :class:`str`
        The token to validate.

    Returns
    -------
    List[:class:`User`, :class:`str`]
        A list containing the user and the token.
    """
    version, *rest = token.split(".")

    if not len(rest):
        raise ValidationError("Invalid token.")

    match version:
        case "v1":
            try:
                id_part, hmac_component = rest
            except ValueError as exc:
                raise ValidationError("Invalid token.") from exc

            return _validate_token_v1(id_part, hmac_component)
        case _:
            raise ValidationError("Invalid token.")
