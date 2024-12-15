from moviepy.editor import VideoFileClip
import os
import re

def remove_opening(opening_seconds):
    video = VideoFileClip(file_name, fps_source="fps")
    video = video.subclip(opening_seconds,video.duration)
    video.write_videofile("gameplay_files/temp.mp4", remove_temp=True)
    video.close()
    os.remove(file_name)
    os.rename("gameplay_files/temp.mp4", file_name)

file_name = "gameplay_files/subway.mp4"

# match_film_folder = re.search(r'([^_]+)_', file_name)
# film_folder = match_film_folder.group(1)
#
# match_season = re.search(r's(\d+)', file_name)
# season = match_season.group(1)
#
# match_episod = re.search(r'e(\d+)', file_name)
# episod = match_episod.group(1)
#
# if os.path.exists(f"C:/Users/Honor/Shorts/films/{film_folder}/{file_name}"):
#     file_name = f"films/{film_folder}/{file_name}"
# else:
#     file_name = f"films/{film_folder}/season{season}/episod{episod}/{file_name}"

remove_opening(30)