import hmac
from base64 import urlsafe_b64decode, urlsafe_b64encode

from server.settings import SECRET_KEY

DEFAULT_ID = "123456789"


def encode_to_b64(data):
    """Encode data to base64."""
    return urlsafe_b64encode(data).decode("utf-8").strip("=")


def decode_from_b64(data):
    """Decode data from base64."""
    return urlsafe_b64decode(data.encode("utf-8")).decode("utf-8")


def generate_token(email, password):
    """Generate a unique token for the user."""
    id_part = encode_to_b64(DEFAULT_ID.encode("utf-8"))

    component = f"{email}:{password}".encode("utf-8")
    key = SECRET_KEY.encode("utf-8")
    signature = encode_to_b64(hmac.new(key, component, "sha256").digest())

    return f"{id_part}.{signature}"
