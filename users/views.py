from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions, generics
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .serializers import PaymentSerializer, RegisterSerializer
from .filters import PaymentFilter
from users.models import User, Payment
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # сортировка по умолчанию по убыванию


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]