import cv2
import os
from moviepy.editor import VideoFileClip, AudioFileClip

# Parameters
image_folder = 'images/'
output_video_path = 'output_video.mp4'
sound_path = 'New fella.mp3'

# Get the list of image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]  # or adjust the file extension
image_files.sort()  # Sort the files for correct ordering

# Get the dimensions of the first image
first_image = cv2.imread(os.path.join(image_folder, image_files[0]))
height, width, layers = first_image.shape

# Initialize VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # specify the codec (e.g., mp4v, xvid, etc.)
out = cv2.VideoWriter(output_video_path, fourcc, 1.0, (width, height))  # adjust frame rate as needed

# Create the video by writing each image to the VideoWriter
for image_filename in image_files:
    img = cv2.imread(os.path.join(image_folder, image_filename))
    out.write(img)

out.release()  # Release the VideoWriter

# Add sound to the video using moviepy
video_clip = VideoFileClip(output_video_path)
audio_clip = AudioFileClip(sound_path)
final_clip = video_clip.set_audio(audio_clip)


# Save the final video with sound
final_clip.write_videofile('final_video.mp4', codec='libx264')

# Clean up intermediate files if needed
video_clip.close()
final_clip.close()
