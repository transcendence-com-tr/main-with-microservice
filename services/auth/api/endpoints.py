
from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth, name='auth'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('me/', views.me, name='me'),
    path("42/", views.login_42, name="login_42"),
    path('42/callback/', views.login_42_callback, name='login_42_callback'),
    path('42/connect/', views.connect_42, name='connect_42'),
    path('2fa/', views.two_factor, name='two_factor'),
    path('2fa/verify/', views.two_factor_verify, name='two_factor_verify'),
    path('password-forgot/', views.password_forgot, name='password_forgot'),
    path('password-reset/', views.password_reset, name='password_reset'),
]