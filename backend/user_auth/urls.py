from django.urls import path, include
from .routers import router
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



urlpatterns = [
path('', include(router.urls)),
path(r"token",  TokenObtainPairView.as_view(), name = "obtain_token"),
path(r"token/refresh",  TokenRefreshView.as_view(), name = "refresh_token"),
path(r"token/verify",  TokenVerifyView.as_view(), name = "verify_token")

]

