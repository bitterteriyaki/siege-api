"""
Siege. All rights reserved
~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022-present Siege Team
:author: Siege Team
"""

from __future__ import annotations

import random

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import (
    BooleanField,
    CharField,
    EmailField,
    SmallIntegerField,
)
from django.utils.translation import gettext as _
from itsdangerous import URLSafeSerializer
from rest_framework.exceptions import ValidationError

from core.models import TimestampedModel


class UserManager(BaseUserManager["User"]):
    """Django requires that custom users define their own manager class.
    By inheriting from `BaseUserManager`, we get a lot of the same code
    used by Django to create a `User` for free.

    All we have to do is override the `create_user` function which we
    will use to create `User` objects.
    """

    def create_user(self, username: str, email: str, password: str) -> User:
        """Create and return a `User` with the email, username and
        password provided.

        Parameters
        ----------
        username: :class:`str`
            The username of the user.
        email: :class:`str`
            The e-mail address of the user.
        password: :class:`str`
            The password of the user.

        Returns
        -------
        :class:`User`
            A new user object with the provided data.
        """
        used_tags = self.values_list("tag", flat=True)
        available_tags = [x for x in range(1, 10_000) if x not in used_tags]

        # If there are no available tags, raise an error.
        if not available_tags:
            raise ValidationError({"username": [_("No available tags.")]})

        tag = random.choice(available_tags)
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, tag=tag)
        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    # Every user has a unique ID that is used to identify them in the
    # database. In this case, we are just telling Mypy that the type
    # of the `id` field is an integer.
    id: int

    # Each `User` needs a human-readable unique identifier that we can
    # use to represent the `User` in the UI. We want to index this
    # column in the database to improve lookup performance.
    username = CharField(db_index=True, max_length=32)

    # We also need a way to contact the user and a way for the user to
    # identify themselves when logging in. Since we need an e-mail
    # address for contacting the user anyways, we will also use the
    # e-mail for logging in because it is the most common form of login
    # credential at the time of writing.
    email = EmailField(db_index=True, max_length=255, unique=True)

    # Each user must have a tag which will permit multiple users to
    # have the same username. The tag will be an integer from 0 to 9999.
    # Users with the same username will not be able to have the same
    # tag.
    tag = SmallIntegerField()

    # When a user no longer wishes to use our platform, they may try to
    # delete there account. That's a problem for us because the data we
    # collect is valuable to us and we don't want to delete it. To solve
    # this problem, we will simply offer users a way to deactivate their
    # account instead of letting them delete it. That way they won't
    # show up on the site anymore, but we can still analyze the data.
    is_active = BooleanField(default=True)

    # The `USERNAME_FIELD` property tells us which field we will use to
    # login. In this case, we want that to be the email field.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Tells Django that the UserManager class defined above should
    # manage objects of this type.
    objects = UserManager()

    class Meta:
        # The name of the table in the database.
        db_table = "users"

    @property
    def token(self) -> str:
        """Returns a token that can be used to authenticate this user.
        As the token has no state, we can generate it at runtime and we
        don't need to store it in the database. This is a convenience
        property that we can use to access the token.

        Returns
        -------
        :class:`str`
            A unique token for the user.
        """
        serializer = URLSafeSerializer(settings.SECRET_KEY, salt="auth")
        token = serializer.dumps(self.id)

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return token
