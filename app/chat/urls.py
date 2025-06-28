from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from django.urls import path

from .views import ThreadViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register(r'threads', ThreadViewSet, basename='thread')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
     path('token/', obtain_auth_token),
] + router.urls
