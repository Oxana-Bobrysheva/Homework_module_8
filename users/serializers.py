from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from users.models import User, Payment

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ["__all__"]


User = get_user_model()

class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = (
            "id"
            "user_name",
            "email",
            "phone",
            "city",
            "avatar",
            "payments",
        )
