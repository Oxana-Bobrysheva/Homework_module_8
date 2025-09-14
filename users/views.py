from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from study.models import Course, Lesson
from users.models import Payment, User
from users.serializers import UserSerializer

from .filters import PaymentFilter
from .serializers import PaymentSerializer, RegisterSerializer
from .stripe_services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "payment_amount"]
    ordering = ["-payment_date"]
    permission_classes = [
        IsAuthenticated
    ]  # Добавлено: только авторизованные пользователи

    def get_queryset(self):

        return Payment.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="create_payment")
    def create_payment(self, request):
        print(request.data)
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")

        if not (course_id or lesson_id):
            return Response(
                {"error": "course_id или lesson_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = request.user

        item = None
        item_name = None
        item_price = None

        try:
            if course_id:
                item = Course.objects.get(id=course_id)
                item_name = item.course_name
                item_price = item.price
            elif lesson_id:
                item = Lesson.objects.get(id=lesson_id)
                item_name = item.lesson_name
                item_price = item.price
        except (Course.DoesNotExist, Lesson.DoesNotExist):
            return Response(
                {"error": "Курс или урок не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        # Создаём платёж в базе
        payment = Payment.objects.create(
            user=user,
            paid_course=item if course_id else None,
            paid_lesson=item if lesson_id else None,
            payment_amount=item_price,  # Используем цену из модели
        )

        try:
            # Интеграция с Stripe
            product_id = create_stripe_product(item_name, f"Оплата за {item_name}")
            price_id = create_stripe_price(product_id, item_price)
            success_url = request.build_absolute_uri("/users/payment/success/")
            cancel_url = request.build_absolute_uri("/users/payment/cancel/")
            session_id, payment_url = create_stripe_session(
                price_id, success_url, cancel_url, user.email
            )

            payment.stripe_session_id = session_id  # Если добавите это поле в модель
            payment.payment_url = payment_url  # Если добавите это поле в модель
            payment.save()

            return Response(
                {
                    "payment_id": payment.id,
                    "payment_url": payment_url,
                },
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            payment.status = "failed"  # Если добавите поле status
            payment.save()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
