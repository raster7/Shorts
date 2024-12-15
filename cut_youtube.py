import random
import re
import shutil
from moviepy.editor import VideoFileClip, clips_array
from subsai import SubsAI
import os
import subprocess


def cut_clips(duration=120):
    video = VideoFileClip(file_name, fps_source="fps")
    gameplay_video = VideoFileClip(f"{shorts_folder}/gameplay_files/{gameplay_file}")
    video_duration = video.duration
    all_clips = []
    clips = []
    gameplay_clips = []
    current_time = 0

    while current_time < video_duration:
        clip_duration = duration
        end_time = min(current_time + clip_duration, video_duration)
        clip = video.subclip(current_time, end_time)
        gameplay_clip = gameplay_video.subclip(current_time, end_time)
        all_clips.append((current_time, end_time, clip, gameplay_clip))
        current_time = end_time

    for i, (start_time, end_time, clip, gameplay_clip) in enumerate(all_clips):
        clip_filename = f"{clips_folder}/clip_p{i+1}.{extension}"
        gameplay_clip_filename = f"{gameplay_folder}/clip_p{i+1}.{extension}"
        clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
        print(f"Сцена с {start_time // 60}:{start_time % 60} - {end_time // 60}:{end_time % 60} сохранена как {clip_filename}")
        clips.append(clip)
        clip_temp = VideoFileClip(clip_filename)
        if clip_temp.duration < 30:
            clip_temp.close()
            os.remove(f"{clips_folder}/clip_p{i+1}.{extension}")
        else:
            gameplay_clip.write_videofile(gameplay_clip_filename, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
            gameplay_clips.append(gameplay_clip)

    return clips, gameplay_clips


def cropp_videos():
    for i in range(counter_of_shorts):
        command = ['ffmpeg', '-y', '-i', f"{clips_folder}/clip_p{i+1}.{extension}", '-vf', 'crop=w=iw-700:h=ih:x=300:y=0',
                    f"{clips_folder}/clip_p{i+1}_cropped.{extension}"]
        subprocess.run(command)
        command = ['ffmpeg', '-y', '-i', f"{gameplay_folder}/clip_p{i+1}.{extension}", '-vf', 'crop=w=iw-700:h=ih:x=300:y=0',
                   f"{gameplay_folder}/clip_p{i+1}_cropped_temp.{extension}"]
        subprocess.run(command)

        clip = VideoFileClip(f"{gameplay_folder}/clip_p{i+1}_cropped_temp.{extension}")
        original_width, original_height = clip.size
        cropped_clip = clip.crop(x1=0, y1=0, x2=original_width, y2=original_height - 100)
        cropped_clip.write_videofile(f"{gameplay_folder}/clip_p{i+1}_cropped.{extension}", codec="libx264", audio_codec="aac")
        clip.close()
        os.remove(f"{gameplay_folder}/clip_p{i+1}_cropped_temp.{extension}")


def merge_videos():
    for i in range(counter_of_shorts):
        video1 = VideoFileClip(f"{clips_folder}/clip_p{i+1}_cropped.{extension}")
        video2 = VideoFileClip(f"{gameplay_folder}/clip_p{i+1}_cropped.{extension}").without_audio()
        temp_merged_video = clips_array([[video1], [video2]])
        temp_merged_video.write_videofile(f"{merged_folder}/merged_video_p{i+1}.{extension}", codec="libx264", audio_codec="aac",
                                     temp_audiofile="temp-audio.m4a", remove_temp=True)


# def convert_to_normal_resolution():
#     for i in range(counter_of_shorts):
#         temp = VideoFileClip(f"{merged_folder}/temp_p{i+1}.{extension}")
#         merged_video = temp.resize(height=1920, width=1080)
#         merged_video.write_videofile(f"{merged_folder}/merged_video_p{i+1}.mp4", codec="libx264", audio_codec="aac")
#         temp.close()
#         #os.remove(f"{merged_folder}/temp_p{i+1}.{extension}")


def add_subtitles():
    for i in range(counter_of_shorts):
        file = f"{merged_folder}/merged_video_p{i+1}.{extension}"
        subs_ai = SubsAI()
        model = subs_ai.create_model('openai/whisper', {'model_type': 'medium'})
        subs = subs_ai.transcribe(file, model)
        subs.save(f"{subtitles_folder}/subtitles_clip_p{i+1}.srt")

        command = [
            'ffmpeg', '-y', '-i', f"{merged_folder}/merged_video_p{i+1}.{extension}",
            '-vf', f"subtitles={subtitles_folder}/subtitles_clip_p{i+1}.srt:force_style='Alignment=2,Fontsize=10,MarginV=127'",
            f"{done_folder}/{done_folder}_p{i+1}.{extension}"
        ]
        subprocess.run(command)

file_name = "moodrenych_v4.mp4"
gameplay_file = "minecraft_v1.mp4"
done_folder = "DONE_SHORTS"
clips_folder = "clips_video"
subtitles_folder = "subtitles_for_clips"
merged_folder = "merged_clips"
gameplay_folder = "clips_gameplay"
shorts_folder = "C:/Users/Honor/Shorts"

extension = file_name.split(".")[-1]

match_video = re.search(r'v(\d+)', file_name)
video = match_video.group(1)

match_video_folder = re.search(r'([^_]+)_', file_name)
video_folder = match_video_folder.group(1)

os.makedirs(f"{shorts_folder}/youtube/{video_folder}/video{video}", exist_ok=True)

if os.path.exists(f"{shorts_folder}/youtube/{video_folder}/{file_name}"):
    shutil.move(f"{shorts_folder}/youtube/{video_folder}/{file_name}",
                f"{shorts_folder}/youtube/{video_folder}/video{video}")

os.chdir(f"{shorts_folder}/youtube/{video_folder}/video{video}")
os.makedirs(clips_folder, exist_ok=True)
os.makedirs(gameplay_folder, exist_ok=True)
os.makedirs(done_folder, exist_ok=True)
os.makedirs(subtitles_folder, exist_ok=True)
os.makedirs(merged_folder, exist_ok=True)

# file_name = f"{shorts_folder}/youtube/{video_folder}/video{video}/episod{episod}/{file_name}"

cut_clips(150)
counter_of_shorts = len([file for file in os.listdir(clips_folder) if os.path.isfile(os.path.join(clips_folder, file))])
cropp_videos()
merge_videos()
extension = 'mp4'
add_subtitles()
