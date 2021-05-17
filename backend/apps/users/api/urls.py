from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'auth', views.AuthViewSet, basename='auth')
router.register(r'', views.UserViewSet, basename='users')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
