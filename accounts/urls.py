from django.urls import path
from accounts import views



app_name = "accounts"

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("refresh-token/", views.RefreshUserTokenAPIView.as_view(), name="refresh"),
]
