import json

from rest_framework.renderers import JSONRenderer


class BaseJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type, renderer_context):
        return json.dumps(data)
