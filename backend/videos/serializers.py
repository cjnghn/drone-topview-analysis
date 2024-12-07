from rest_framework import serializers
from .models import Video, Tracking, Frame, Detection, Intersection


class VideoListSerializer(serializers.ModelSerializer):
    tracking_count = serializers.IntegerField(read_only=True)
    frame_count = serializers.IntegerField(read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "title",
            "file",
            "start_time",
            "end_time",
            "start_latitude",
            "start_longitude",
            "end_latitude",
            "end_longitude",
            "tracking_count",
            "frame_count",
            "duration",
        ]

    def get_duration(self, obj):
        return obj.end_time - obj.start_time


class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = [
            "id",
            "video",
            "track_id",
            "frame_start",
            "frame_end",
            "start_point",
            "end_point",
            "timestamp_start",
            "timestamp_end",
        ]


class DetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = [
            "id",
            "frame",
            "tracking",
            "class_id",
            "bbox",
            "confidence",
            "world_speed",
            "latitude",
            "longitude",
        ]


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = [
            "id",
            "video",
            "frame_index",
            "timestamp",
            "latitude",
            "longitude",
            "altitude",
            "heading",
        ]


class IntersectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = [
            "id",
            "video",
            "track1",
            "track2",
            "frame_index",
            "timestamp",
            "intersection_point",
            "intersection_point_type",
            "latitude",
            "longitude",
            "time_difference",
        ]
