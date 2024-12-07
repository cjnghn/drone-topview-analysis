from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from .models import Video, Tracking, Frame, Detection, Intersection
from .serializers import (
    VideoListSerializer,
    TrackingSerializer,
    FrameSerializer,
    IntersectionSerializer,
)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.annotate(
        tracking_count=Count("tracking"), frame_count=Count("frames")
    )
    serializer_class = VideoListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["title"]

    @action(detail=True, methods=["get"])
    def track_positions(self, request, pk=None):
        """특정 timestamp의 모든 tracking 위치 조회"""
        timestamp = float(request.query_params.get("timestamp", 0))
        tracks = (
            Detection.objects.filter(
                frame__video_id=pk, frame__timestamp__lte=timestamp
            )
            .values("tracking_id")
            .annotate(
                last_latitude=Avg("latitude"),
                last_longitude=Avg("longitude"),
                last_speed=Avg("world_speed"),
            )
        )
        return Response(list(tracks))


class TrackingViewSet(viewsets.ModelViewSet):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video", "track_id"]

    @action(detail=True, methods=["get"])
    def trajectory(self, request, pk=None):
        """트래킹의 전체 이동 경로"""
        detections = (
            Detection.objects.filter(tracking_id=pk)
            .order_by("frame__timestamp")
            .values("frame__timestamp", "latitude", "longitude", "world_speed")
        )
        return Response(list(detections))


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video", "frame_index"]

    @action(detail=True, methods=["get"])
    def detections(self, request, pk=None):
        """프레임의 모든 detection 정보"""
        detections = Detection.objects.filter(frame_id=pk).values(
            "tracking_id",
            "class_id",
            "bbox",
            "confidence",
            "world_speed",
            "latitude",
            "longitude",
        )
        return Response(list(detections))


class IntersectionViewSet(viewsets.ModelViewSet):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video", "track1", "track2"]

    @action(detail=False, methods=["get"])
    def time_range(self, request):
        """시간 범위 내의 모든 교차점"""
        video_id = request.query_params.get("video_id")
        start_time = float(request.query_params.get("start_time", 0))
        end_time = float(request.query_params.get("end_time", 0))

        intersections = self.queryset.filter(
            video_id=video_id, timestamp__gte=start_time, timestamp__lte=end_time
        ).order_by("timestamp")

        return Response(self.get_serializer(intersections, many=True).data)
