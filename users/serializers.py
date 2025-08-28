from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_name",
            "email",
            "phone",
            "city",
            "avatar",
        )
