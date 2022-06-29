from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import AccountView
from rest_framework_simplejwt import views

urlpatterns = [
    path('token-auth/', obtain_auth_token),
    path('accounts', AccountView.as_view()),
    path("token-jwt/", views.TokenObtainPairView.as_view()),
    path("token-jwt/refresh/", views.TokenRefreshView.as_view()),
]