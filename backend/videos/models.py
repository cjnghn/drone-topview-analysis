from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="videos/")
    start_time = models.FloatField()
    end_time = models.FloatField()
    start_latitude = models.FloatField()
    start_longitude = models.FloatField()
    end_latitude = models.FloatField()
    end_longitude = models.FloatField()

    def __str__(self):
        return self.title


class Tracking(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="tracking")
    track_id = models.IntegerField()
    frame_start = models.IntegerField()
    frame_end = models.IntegerField()
    start_point = models.JSONField()
    end_point = models.JSONField()
    timestamp_start = models.FloatField()
    timestamp_end = models.FloatField()

    class Meta:
        unique_together = ("video", "track_id")

    def __str__(self):
        return f"Track {self.track_id} in Video {self.video.title}"


class Frame(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="frames")
    frame_index = models.IntegerField()
    timestamp = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    heading = models.FloatField()

    def __str__(self):
        return f"Frame {self.frame_index} in Video {self.video.title}"


class Detection(models.Model):
    frame = models.ForeignKey(
        Frame, on_delete=models.CASCADE, related_name="detections"
    )
    tracking = models.ForeignKey(
        Tracking, on_delete=models.CASCADE, related_name="detections"
    )
    class_id = models.IntegerField()
    bbox = models.JSONField()
    confidence = models.FloatField()
    world_speed = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Detection in Frame {self.frame.frame_index} - Track {self.tracking.track_id}"


class Intersection(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="intersections"
    )
    track1 = models.ForeignKey(
        Tracking, on_delete=models.CASCADE, related_name="track1_intersections"
    )
    track2 = models.ForeignKey(
        Tracking, on_delete=models.CASCADE, related_name="track2_intersections"
    )
    frame_index = models.IntegerField()
    timestamp = models.FloatField()
    intersection_point = models.JSONField()
    intersection_point_type = models.CharField(
        max_length=50, default="center"
    )  # 교차점 유형
    latitude = models.FloatField()
    longitude = models.FloatField()
    time_difference = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=["video", "track1", "track2"]),
        ]

    def __str__(self):
        return f"Intersection between Track {self.track1.track_id} and Track {self.track2.track_id} in Video {self.video.title}"
