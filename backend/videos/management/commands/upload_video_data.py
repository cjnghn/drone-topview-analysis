import os
import json
import shutil
from tqdm import tqdm
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from videos.models import Video, Frame, Detection, Tracking, Intersection


class Command(BaseCommand):
    help = "Upload video and JSON data into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--json", type=str, required=True, help="Path to the JSON file."
        )
        parser.add_argument(
            "--video", type=str, required=True, help="Path to the video file."
        )

    def handle(self, *args, **options):
        json_path = options["json"]
        video_path = options["video"]

        # Check if files exist
        if not os.path.exists(json_path):
            raise CommandError(f"JSON file not found: {json_path}")
        if not os.path.exists(video_path):
            raise CommandError(f"Video file not found: {video_path}")

        # Load JSON data
        with open(json_path, "r") as f:
            data = json.load(f)

        # Save video data
        video_filename = os.path.basename(video_path)
        
        # Check if video already exists
        video = Video.objects.filter(title=video_filename).first()
        if video:
            self.stdout.write(
                f"Video '{video_filename}' already exists, using existing record."
            )
        else:
            # Create videos directory if it doesn't exist
            videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
            os.makedirs(videos_dir, exist_ok=True)
            
            # Copy video file to media directory
            dest_path = os.path.join(videos_dir, video_filename)
            shutil.copy2(video_path, dest_path)
            
            # Create video record
            with open(dest_path, 'rb') as video_file:
                video = Video.objects.create(
                    title=video_filename,
                    file=File(video_file, name=video_filename),
                    start_time=data["start_time"],
                    end_time=data["end_time"],
                    start_latitude=data["start_location"]["latitude"],
                    start_longitude=data["start_location"]["longitude"],
                    end_latitude=data["end_location"]["latitude"],
                    end_longitude=data["end_location"]["longitude"],
                )
            self.stdout.write(f"Video '{video_filename}' added.")

        # Save tracking data
        self.stdout.write("Processing tracking data...")
        tracking_map = {}
        for tracking_data in tqdm(data["tracking"], desc="Tracking", unit="track"):
            tracking, created = Tracking.objects.get_or_create(
                video=video,
                track_id=tracking_data["track_id"],
                defaults={
                    "frame_start": tracking_data["frame_start"],
                    "frame_end": tracking_data["frame_end"],
                    "start_point": tracking_data["start_point"],
                    "end_point": tracking_data["end_point"],
                    "timestamp_start": tracking_data["timestamp_start"],
                    "timestamp_end": tracking_data["timestamp_end"],
                },
            )
            tracking_map[tracking_data["track_id"]] = tracking

        # Save frames and detections
        self.stdout.write("Processing frames and detections...")
        for frame_data in tqdm(data["frames"], desc="Frames", unit="frame"):
            frame = Frame.objects.create(
                video=video,
                frame_index=frame_data["frame_index"],
                timestamp=frame_data["timestamp"],
                latitude=frame_data["drone_state"]["latitude"],
                longitude=frame_data["drone_state"]["longitude"],
                altitude=frame_data["drone_state"]["altitude"],
                heading=frame_data["drone_state"]["heading"],
            )

            for detection_data in frame_data["detections"]:
                track_id = detection_data.get("track_id")
                if track_id not in tracking_map:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping detection with missing track_id: {track_id}"
                        )
                    )
                    continue

                Detection.objects.create(
                    frame=frame,
                    tracking=tracking_map[track_id],
                    class_id=detection_data["class_id"],
                    bbox=detection_data["bbox"],
                    confidence=detection_data["confidence"],
                    world_speed=detection_data["world_speed"],
                    latitude=detection_data["gps_coordinates"]["latitude"],
                    longitude=detection_data["gps_coordinates"]["longitude"],
                )

        # Save intersections
        self.stdout.write("Processing intersections...")
        for intersection_data in tqdm(
            data["intersections"], desc="Intersections", unit="intersection"
        ):
            track1 = tracking_map.get(intersection_data["track_id1"])
            track2 = tracking_map.get(intersection_data["track_id2"])

            if not track1 or not track2:
                self.stdout.write(
                    self.style.WARNING(
                        "Skipping intersection with missing track1 or track2."
                    )
                )
                continue

            Intersection.objects.create(
                video=video,
                track1=track1,
                track2=track2,
                frame_index=intersection_data["frame_index"],
                timestamp=intersection_data["timestamp"],
                intersection_point=intersection_data["intersection_point"],
                latitude=intersection_data["gps_coordinates"]["latitude"],
                longitude=intersection_data["gps_coordinates"]["longitude"],
                time_difference=intersection_data["time_difference"],
            )

        self.stdout.write(self.style.SUCCESS("Data upload complete."))