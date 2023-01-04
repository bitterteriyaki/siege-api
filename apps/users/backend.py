import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime

from snowflake import SnowflakeGenerator

from server.settings import SECRET_KEY

# NOTE:
# This is a dummy ID, the application will implement a real ID
# generation mechanism (Snowflake IDs) further, this is just to show
# how the token is generated.
DEFAULT_ID = "123456789"


def encode_to_b64(data):
    """Encode data to base64."""
    return urlsafe_b64encode(data).decode("utf-8").strip("=")


def decode_from_b64(data):
    """Decode data from base64."""
    return urlsafe_b64decode(data.encode("utf-8")).decode("utf-8")


def _generate_token_v1(email, password):
    signature = f"{email}.{password}".encode("utf-8")
    message = encode_to_b64(signature).encode("utf-8")

    key = SECRET_KEY.encode("utf-8")

    hmac_component = encode_to_b64(hmac.new(key, message, "sha256").digest())
    id_part = encode_to_b64(DEFAULT_ID.encode("utf-8"))

    return f"v1.{id_part}.{hmac_component}"


def generate_token(email, password, version="v1"):
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
    email: :class:`str`
        The e-mail of the user.
    password: :class:`str`
        The password of the user.

    Returns
    -------
    :class:`str`
        A unique token for the user.

    Notes
    -----
    The ID is a dummy ID, the application will implement a real ID
    generation mechanism (Snowflake IDs) further, this is just to show
    how the token is generated.
    """
    match version:
        case "v1":
            return _generate_token_v1(email, password)


epoch = int(datetime(2023, 1, 1, 0, 0, 0, 0).timestamp())
id_generator = SnowflakeGenerator(42, epoch=epoch)
