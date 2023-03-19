from json import JSONDecoder, JSONEncoder
from typing import Any, Sequence

from pusher.http import Request

class Pusher:
    def __init__(
        self,
        app_id: str,
        key: str,
        secret: str,
        ssl: bool = ...,
        host: str | None = ...,
        port: int | None = ...,
        timeout: int | None = ...,
        cluster: str | None = ...,
        encryption_master_key: str | None = ...,
        encryption_master_key_base64: str | None = ...,
        json_encoder: type[JSONEncoder] | None = ...,
        json_decoder: type[JSONDecoder] | None = ...,
        backend: type[object] | None = ...,
        **backend_options: Any,
    ) -> None: ...
    def trigger(
        self,
        channels: str | Sequence[str],
        event_name: str,
        data: Any,
        socket_id: str | None = ...,
    ) -> Request: ...
