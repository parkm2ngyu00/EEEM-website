from django.urls import path
from account import views

urlpatterns = [
    path("logout/", views.logout_view, name="logout"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
]
