from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import AnimalView, AnimalDetailView

urlpatterns = [
    path("animals/<int:animal_id>/", AnimalDetailView.as_view()),
    path("animals/", AnimalView.as_view()),
    # Acessa o download do schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Opcionais
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]