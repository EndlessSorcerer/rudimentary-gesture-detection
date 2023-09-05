from rest_framework import serializers
from .models import Video
from noddingpigeon.inference import predict_video
from noddingpigeon.video import VideoSegment  # Optional.
import os

def process_video(video_path):
    # Open the video file
    print(video_path)
    try:
        result = predict_video(
            os.path.abspath(video_path),
            video_segment=VideoSegment.LAST,  # Optionally change these parameters.
            motion_threshold=0.5,
            gesture_threshold=0.9
        )
    # Continue with the code to handle the result
    except Exception as e:
    # Handle the exception or error case
        print("An error occurred during video prediction:", str(e))
    print(result)
    return result

def process_uploaded_video(video):
    # Get the video file path
    video_path = video.video_file.path

    # Process the video
    processed_result = process_video(video_path)

    # Update the processed_result field of the Video model
    if processed_result is not None:
        # Convert processed_result to a string or save it in a different format
        processed_result_str = str(processed_result)
        print(processed_result_str)
        video.processed_result = processed_result_str
        print(video.processed_result)
        # video.save()
    return processed_result


class VideoSerializer(serializers.ModelSerializer):
    processed_result = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Video
        fields = '__all__'
    # def create(self, validated_data):
    #     video = Video.objects.create(**validated_data)
    #     processed_result = process_uploaded_video(video)  # Process the uploaded video
    #     video.processed_result = processed_result
    #     video.save()

    #     # Customize the response data
    #     response_data = {
    #         'id': video.id,
    #         'title': video.title,
    #         'video_file': video.video_file.url,
    #         'uploaded_at': video.uploaded_at,
    #         'processed_result': video.processed_result,
    #     }
    #     return response_data