from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'meet', views.MeetViewSet, basename='Meet')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
