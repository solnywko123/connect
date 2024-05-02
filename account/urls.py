
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [

    path('', views.UserListView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('activate/', views.ActivationView.as_view()),
    path('register_phone/', views.RegistrationPhoneView.as_view()),  # Новый URL для активации по номеру телефона
    path('activate/phone/', views.ActivationPhoneView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

]