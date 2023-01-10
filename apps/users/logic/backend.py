"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode

from django.conf import settings
from rest_framework.exceptions import ValidationError


def encode_to_b64(data):
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


def decode_from_b64(data):
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


def _generate_token_v1(user_id, email, password):
    signature = f"{email}.{password}".encode("utf-8")
    message = encode_to_b64(signature).encode("utf-8")

    key = settings.SECRET_KEY.encode("utf-8")

    hmac_component = encode_to_b64(hmac.new(key, message, "sha256").digest())
    id_part = encode_to_b64(user_id.encode("utf-8"))

    return (id_part, hmac_component)


def generate_token(user_id, email, password, version="v1"):
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


def _validate_token_v1(id_part, hmac_component):
    # to avoid circular imports
    from apps.users.models import User

    user_id = decode_from_b64(id_part).decode("utf-8")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist as exc:
        raise ValidationError("Invalid token.") from exc

    _, expected = _generate_token_v1(user_id, user.email, user.password)

    expected = decode_from_b64(expected)
    hmac_component = decode_from_b64(hmac_component)

    if not hmac.compare_digest(hmac_component, expected):
        raise ValidationError("Invalid token.")

    return (user, user.token)


def validate_token(token):
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
    try:
        version, *rest = token.split(".")
    except ValueError as exc:
        raise ValidationError("Invalid token.") from exc

    match version:
        case "v1":
            try:
                id_part, hmac_component = rest
            except ValueError as exc:
                raise ValidationError("Invalid token.") from exc

            return _validate_token_v1(id_part, hmac_component)
