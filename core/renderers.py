from rest_framework.renderers import JSONRenderer


class BaseJSONRenderer(JSONRenderer):
    charset = "utf-8"


class UserJSONRenderer(BaseJSONRenderer):
    def render(self, data, accepted_media_type, renderer_context):
        if data.get("errors") is not None:
            renderer_context["response"].data = data["errors"]
            return super().render(data["errors"])

        data["id"] = str(data["id"])
        data["tag"] = str(data["tag"]).zfill(4)

        return super().render(data, accepted_media_type, renderer_context)
