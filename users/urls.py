from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r'payments', PaymentViewSet, basename='payment')
urlpatterns = [path('api/', include(router.urls)),]

urlpatterns += router.urls
