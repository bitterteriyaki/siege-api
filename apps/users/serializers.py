from rest_framework.serializers import CharField, ModelSerializer

from apps.users.models import User


class UsersSerializer(ModelSerializer):
    """Serializer for the `/users` route. This serializer is responsible
    for validating the data sent to the `/users` route and for
    serializing the data returned by the same route.

    These are the fields that are validated:
    - `username`: must be a string between 2 and 32 characters long.
    - `password`: must be a string between 8 and 128 characters long.
    - `email`: must be a valid e-mail address.
    - `tag`: must be a string between 1 and 4 characters long.
    """

    # Username should have a minimum length of 2 characters and a
    # maximum length of 32 characters.
    username = CharField(min_length=2, max_length=32)

    # The password should have a minimum length of 8 characters and a
    # maximum length of 128 characters, and it is also write-only so
    # that it is not returned in the response.
    password = CharField(min_length=8, max_length=128, write_only=True)

    # The user token should be a string with a maximum length of 255
    # characters and it is also read-only so that it is not included
    # in the request.
    token = CharField(max_length=255, read_only=True)

    # The user should not be able to set the tag, so it is also
    # read-only.
    tag = CharField(max_length=4, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a
        # request or response, including fields specified explicitly
        # above.
        fields = [
            "id",
            "username",
            "email",
            "password",
            "tag",
            "token",
            "created_at",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
