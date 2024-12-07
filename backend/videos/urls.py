# urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VideoViewSet, TrackingViewSet, FrameViewSet, IntersectionViewSet

router = DefaultRouter()
router.register(r"videos", VideoViewSet)
router.register(r"tracking", TrackingViewSet)
router.register(r"frames", FrameViewSet)
router.register(r"intersections", IntersectionViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
