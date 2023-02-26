"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound

from apps.users.models import User


def get_user(user_id: int) -> User:
    """Get an user by is ID. If the user does no exist raise a
    :class:`NotFound` exception.

    Parameters
    ----------
    user_id: :class:`int`
        The ID of the user to get.

    Returns
    -------
    :class:`User`
        The user with the given ID.

    Raises
    ------
    :class:`NotFound`
        If the user does not exist.
    """
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist as exc:
        raise NotFound(_("User not found.")) from exc
