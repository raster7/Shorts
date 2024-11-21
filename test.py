import random
import re
import shutil
import os
from moviepy.editor import VideoFileClip, clips_array
from subsai import SubsAI
import os
import subprocess

def remove_opening():
    video = VideoFileClip(file_name, fps_source="fps")
    video = video.subclip(10,30)
    video.write_videofile("temp.mp4" ,remove_temp=True)
    video.close()
    os.remove(file_name)
    os.rename("temp.mp4", file_name)

file_name = "1111.mp4"
subway_file = "subway_files/subway.mp4"
done_folder = "DONE_SHORTS"
clips_folder = "clips_video"
subtitles_folder = "subtitles_for_clips"
merged_folder = "merged_clips"
subway_folder = "clips_subway"
shorts_folder = "C:/Users/Honor/Shorts"

remove_opening()