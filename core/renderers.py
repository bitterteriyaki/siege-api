from rest_framework.renderers import JSONRenderer


class BaseJSONRenderer(JSONRenderer):
    """Base JSON renderer class. All other JSON renderers should inherit
    from this class. This class is responsible for setting the default
    encoding to `utf-8`, this is required for the `JSONRenderer` class
    to work properly.

    Please note that this class is not a renderer itself, it is just
    a base class for other renderers to inherit from.
    """

    charset = "utf-8"


class UserJSONRenderer(BaseJSONRenderer):
    """Renderer for the :class:`User` model. This renderer will
    render the :class:`User` model into JSON format.

    - `id` will be converted to a string.
    - `tag` will be converted to a string and padded with zeros.

    If the `User` model has any errors, the `errors` key will be
    rendered instead of the `User` model.
    """

    def render(self, data, accepted_media_type, renderer_context):
        if data.get("errors") is not None:
            renderer_context["response"].data = data["errors"]
            return super().render(data["errors"])

        data["id"] = str(data["id"])
        data["tag"] = str(data["tag"]).zfill(4)

        return super().render(data, accepted_media_type, renderer_context)
