"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

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
