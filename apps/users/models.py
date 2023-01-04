import random

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

from apps.users.backend import generate_token
from core.models import TimestampedModel


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code
    used by Django to create a `User` for free.

    All we have to do is override the `create_user` function which we
    will use to create `User` objects.
    """

    def create_user(self, username, email, password):
        """Create and return a `User` with an email, username and
        password.
        """
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an e-mail address.")

        if password is None:
            raise TypeError("Users must have a password.")

        used_tags = self.values_list("tag", flat=True)
        available_tags = [x for x in range(1, 10000) if x not in used_tags]

        if not available_tags:
            raise ValueError("No available tags.")

        tag = random.choice(available_tags)
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, tag=tag)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Create and return a `User` with superuser powers.

        Superuser powers means that this use is an admin that can do
        anything they want.
        """
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    # Each `User` needs a human-readable unique identifier that we can
    # use to represent the `User` in the UI. We want to index this
    # column in the database to improve lookup performance.
    username = CharField(db_index=True, max_length=255)

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
    tag = SmallIntegerField(db_index=True)

    # When a user no longer wishes to use our platform, they may try to
    # delete there account. That's a problem for us because the data we
    # collect is valuable to us and we don't want to delete it. To solve
    # this problem, we will simply offer users a way to deactivate their
    # account instead of letting them delete it. That way they won't
    # show up on the site anymore, but we can still analyze the data.
    is_active = BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and
    # cannot log into the Django admin site. For most users, this flag
    # will always be falsed.
    is_staff = BooleanField(default=False)

    # The `USERNAME_FIELD` property tells us which field we will use to
    # login. In this case, we want that to be the email field.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Tells Django that the UserManager class defined above should
    # manage objects of this type.
    objects = UserManager()

    def __str__(self):
        """Return a human readable representation of the model instance.
        The representation format will be `<username>#<tag>`.
        """
        return f"{self.username}#{self.tag:04}"

    @property
    def token(self):
        """Returns a token that can be used to authenticate this user.
        As the token has no state, we can generate it at runtime and we
        don't need to store it in the database. This is a convenience
        property that we can use to access the token.

        Returns
        -------
        :class:`str`
            A unique token for the user.
        """
        return generate_token(self.email, self.password)
