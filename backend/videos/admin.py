from django.contrib import admin
from .models import Video, Frame, Detection, Tracking, Intersection


class FrameInline(admin.TabularInline):
    model = Frame
    extra = 0
    fields = (
        "frame_index",
        "timestamp",
        "latitude",
        "longitude",
        "altitude",
        "heading",
    )


class DetectionInline(admin.TabularInline):
    model = Detection
    extra = 0
    fields = ("class_id", "confidence", "world_speed", "latitude", "longitude")


class TrackingInline(admin.TabularInline):
    model = Tracking
    extra = 0
    fields = (
        "track_id",
        "frame_start",
        "frame_end",
        "timestamp_start",
        "timestamp_end",
        "start_point",
        "end_point",
    )


class IntersectionInline(admin.TabularInline):
    model = Intersection
    extra = 0
    fields = (
        "track1",
        "track2",
        "timestamp",
        "latitude",
        "longitude",
        "time_difference",
    )


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "start_time",
        "end_time",
        "start_latitude",
        "start_longitude",
        "end_latitude",
        "end_longitude",
    )
    inlines = [FrameInline, TrackingInline, IntersectionInline]


@admin.register(Frame)
class FrameAdmin(admin.ModelAdmin):
    list_display = (
        "video",
        "frame_index",
        "timestamp",
        "latitude",
        "longitude",
        "altitude",
        "heading",
    )
    search_fields = ("video__title", "frame_index")


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = (
        "video",
        "track_id",
        "frame_start",
        "frame_end",
        "timestamp_start",
        "timestamp_end",
    )
    inlines = [DetectionInline]


@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = (
        "frame",
        "tracking",
        "class_id",
        "confidence",
        "world_speed",
        "latitude",
        "longitude",
    )


@admin.register(Intersection)
class IntersectionAdmin(admin.ModelAdmin):
    list_display = (
        "video",
        "track1",
        "track2",
        "frame_index",
        "timestamp",
        "latitude",
        "longitude",
        "time_difference",
    )
    search_fields = ("track1__track_id", "track2__track_id")
    list_filter = ("video",)
