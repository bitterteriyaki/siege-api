from rest_framework.renderers import JSONRenderer


class BaseJSONRenderer(JSONRenderer):
    charset = "utf-8"


class UserJSONRenderer(BaseJSONRenderer):
    def render(self, data, accepted_media_type, renderer_context):
        data["id"] = str(data["id"])
        data["tag"] = str(data["tag"]).zfill(4)

        return super().render(data, accepted_media_type, renderer_context)
