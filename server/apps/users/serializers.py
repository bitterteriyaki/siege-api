from rest_framework.serializers import CharField, ModelSerializer

from server.apps.users.models import User


class UsersSerializer(ModelSerializer):
    username = CharField(min_length=2, max_length=32)
    password = CharField(min_length=8, max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)
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
