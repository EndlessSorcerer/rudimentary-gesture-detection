from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import VideoViewSet

router = routers.DefaultRouter()
router.register(r'videos', VideoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
