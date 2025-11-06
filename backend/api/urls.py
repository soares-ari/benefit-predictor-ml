"""URL configuration for API endpoints."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health_check, predict_view, PredictionViewSet, EmployeeProfileViewSet

# Router para ViewSets
router = DefaultRouter()
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'employees', EmployeeProfileViewSet, basename='employee')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('predict/', predict_view, name='predict'),
    path('', include(router.urls)),
]