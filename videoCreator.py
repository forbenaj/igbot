from moviepy.editor import VideoFileClip, AudioFileClip, ImageSequenceClip, concatenate_videoclips
import os

def create_video(fileNames,durations):
    # Paths to your images and sound file
    image_folder = 'images'
    sound_file = 'output.mp3'

    # List of image filenames in the folder
    #image_files = [f"{image_folder}/{img}" for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
    #image_files = os.listdir(image_folder)



    # Duration for each image in seconds
    image_duration = 2  # Adjust as needed

    # Load the sound clip
    audio_clip = AudioFileClip(sound_file)

    # Create an ImageSequenceClip from the images with specified durations
    #image_clips = [ImageSequenceClip([f"images/{img}"], durations=[image_files.index(img)]) for img in image_files]

    image_clips = ImageSequenceClip(fileNames,durations=durations)


    # Set the audio for the video
    image_clips = image_clips.set_audio(audio_clip)

    # Write the final video to a file
    output_video_path = 'output_video.mp4'
    image_clips.write_videofile(output_video_path, codec="libx264",fps=30)
