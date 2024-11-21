import random
import re
import shutil
from moviepy.editor import VideoFileClip, clips_array
from subsai import SubsAI
import os
import subprocess


def cut_clips():
    video = VideoFileClip(f"{file_name}", fps_source="fps")
    subway_video = VideoFileClip(f"{shorts_folder}/subway_files/{subway_file}")
    video_duration = video.duration
    min_duration = 55
    max_duration = 65
    all_clips = []
    clips = []
    subway_clips = []
    current_time = 0

    while current_time < video_duration:
        clip_duration = random.randint(min_duration, max_duration)
        end_time = min(current_time + clip_duration, video_duration)
        clip = video.subclip(current_time, end_time)
        subway_clip = subway_video.subclip(current_time, end_time)
        all_clips.append((current_time, end_time, clip, subway_clip))
        current_time = end_time

    for i, (start_time, end_time, clip, subway_clip) in enumerate(all_clips):
        clip_filename = f"clip_p{i}.mkv"
        subway_clip_filename = clip_filename
        clip.write_videofile(clips_folder + '/' + clip_filename, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
        subway_clip.write_videofile(subway_folder + '/' + subway_clip_filename, codec="libx264", audio_codec="aac",
                             temp_audiofile="temp-audio.m4a", remove_temp=True)
        print(f"Сцена с {start_time // 60}:{start_time % 60} - {end_time // 60}:{end_time % 60} сохранена как {clip_filename}")
        clips.append(clip)
        subway_clips.append(subway_clip)

    return clips, subway_clips


def cropp_videos():
    for i in range(counter_of_shorts):
        command = ['ffmpeg', '-y', '-i', f"{clips_folder}/clip_p{i}.{extension}", '-vf', 'crop=w=iw-700:h=ih:x=300:y=0',
                    f"{clips_folder}/clip_p{i}_cropped.{extension}"]
        subprocess.run(command)
        command = ['ffmpeg', '-y', '-i', f"{subway_folder}/clip_p{i}.{extension}", '-vf', 'crop=w=iw-700:h=ih:x=300:y=0',
                   f"{subway_folder}/clip_p{i}_cropped.{extension}"]
        subprocess.run(command)


def merge_videos():
    for i in range(counter_of_shorts):
        video1 = VideoFileClip(f"{clips_folder}/clip_p{i}_cropped.{extension}")
        video2 = VideoFileClip(f"{subway_folder}/clip_p{i}_cropped.{extension}").without_audio()
        merged_video = clips_array([[video1], [video2]])
        merged_video.write_videofile(f"{merged_folder}/merged_video_p{i}.{extension}", codec="libx264", audio_codec="aac",
                                     temp_audiofile="temp-audio.m4a", remove_temp=True)

def add_subtitles():
    for i in range(counter_of_shorts):
        file = f"{merged_folder}/merged_video_p{i}.{extension}"
        subs_ai = SubsAI()
        model = subs_ai.create_model('openai/whisper', {'model_type': 'tiny'})
        subs = subs_ai.transcribe(file, model)
        subs.save(f"{subtitles_folder}/subtitles_clip_p{i}.srt")

        command = [
            'ffmpeg', '-y', '-i', f"{merged_folder}/merged_video_p{i}.{extension}",
            '-vf', f"subtitles={subtitles_folder}/subtitles_clip_p{i}.srt:force_style='Alignment=2,Fontsize=10,MarginV=135'",
            f"{done_folder}/{done_folder}_p{i}.{extension}"
        ]
        subprocess.run(command)

file_name = "thekitchen_e1s1.mkv"
subway_file = "subway_1080.mp4"
done_folder = "DONE_SHORTS"
clips_folder = "clips_video"
subtitles_folder = "subtitles_for_clips"
merged_folder = "merged_clips"
subway_folder = "clips_subway"
shorts_folder = "C:/Users/Honor/Shorts"

extension = file_name.split(".")[-1]

match_season = re.search(r's(\d+)', file_name)
season = match_season.group(1)

match_episod = re.search(r'e(\d+)', file_name)
episod = match_episod.group(1)

match_film_folder = re.search(r'([^_]+)_', file_name)
film_folder = match_film_folder.group(1)

os.makedirs(f"{shorts_folder}/films/{film_folder}/season{season}", exist_ok=True)
os.makedirs(f"{shorts_folder}/films/{film_folder}/season{season}/episod{episod}", exist_ok=True)

if os.path.exists(f"{shorts_folder}/films/{film_folder}/{file_name}"):
    shutil.move(f"{shorts_folder}/films/{film_folder}/{file_name}",
                f"{shorts_folder}/films/{film_folder}/season{season}/episod{episod}")

os.chdir(f"{shorts_folder}/films/{film_folder}/season{season}/episod{episod}")
os.makedirs(clips_folder, exist_ok=True)
os.makedirs(subway_folder, exist_ok=True)
os.makedirs(done_folder, exist_ok=True)
os.makedirs(subtitles_folder, exist_ok=True)
os.makedirs(merged_folder, exist_ok=True)

# file_name = f"{shorts_folder}/films/{film_folder}/season{season}/episod{episod}/{file_name}"
counter_of_shorts = len([file for file in os.listdir(clips_folder) if os.path.isfile(os.path.join(clips_folder, file))])

cut_clips()
cropp_videos()
merge_videos()
add_subtitles()
