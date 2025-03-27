from django.urls import path
from .views import predict_fault,register_page, login_page, register, login, logout

urlpatterns = [
    path("predict/", predict_fault, name="predict_form"),
    path("register/", register_page, name="register_page"),
    path("", login_page, name="login_page"),
    path("api/register/", register, name="register"),
    path("api/login/", login, name="login"),
    path("logout/", logout, name="logout"),
]