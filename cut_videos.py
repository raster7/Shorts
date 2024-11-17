import random
import os
from moviepy.editor import VideoFileClip, clips_array
from subsai import SubsAI
import os
import subprocess


def cut_clips(video_file, subway_file, min_duration=40, max_duration=60):
    # temp_file = "1.mp4"
    # command = [
    #     "ffmpeg", "-i", video_file, "-c:v", "copy", "-c:a", "copy", "-y", temp_file
    # ]
    # subprocess.run(command)
    # os.replace(temp_file, video_file)

    video = VideoFileClip(video_file, fps_source="fps")
    subway_video = VideoFileClip(subway_file)
    video_duration = video.duration

    all_clips = []

    current_time = 0
    while current_time < video_duration:
        clip_duration = random.randint(min_duration, max_duration)
        end_time = min(current_time + clip_duration, video_duration)
        clip = video.subclip(current_time, end_time)
        subway_clip = subway_video.subclip(current_time, end_time)
        all_clips.append((current_time, end_time, clip, subway_clip))
        current_time = end_time

    clips = []
    subway_clips = []

    for i, (start_time, end_time, clip, subway_clip) in enumerate(all_clips):
        clip_filename = f"clip{i}.mp4"
        subway_clip_filename = f"subway_clip{i}.mp4"
        shorts_folder = video_file.replace('.mp4','',1)
        subway_shorts_folder = subway_file.replace('.mp4', '', 1)

        os.makedirs(shorts_folder, exist_ok=True)
        os.makedirs(subway_shorts_folder, exist_ok=True)

        clip.write_videofile(shorts_folder + '/' + clip_filename, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
        subway_clip.write_videofile(subway_shorts_folder + '/' + subway_clip_filename, codec="libx264", audio_codec="aac",
                             temp_audiofile="temp-audio.m4a", remove_temp=True)

        print(
            f"Сцена с {start_time // 60}:{start_time % 60} - {end_time // 60}:{end_time % 60} сохранена как {clip_filename}")

        clips.append(clip)
        subway_clips.append(subway_clip)

    return clips, subway_clips


video_file = "2222.mp4"
subway_file = "subwayserf.mp4"
cut_clips(video_file, subway_file, min_duration=40, max_duration=60)
shorts_folder = "0101"
subway_folder = "subwayserf"
shorts_sub_folder = "0101sub"
os.makedirs(shorts_sub_folder, exist_ok=True)
shorts_done_folder = "0101done"
os.makedirs(shorts_done_folder, exist_ok=True)
shorts_merged_folder = "0101merged"
os.makedirs(shorts_merged_folder, exist_ok=True)
counter = len([file for file in os.listdir(shorts_folder) if os.path.isfile(os.path.join(shorts_folder, file))])
for i in range(counter):
    command1 = ['ffmpeg', '-y', '-i', f"{shorts_folder}/clip{i}.mp4", '-vf', 'crop=w=iw-250:h=ih:x=100:y=0',
                f"{shorts_folder}/clip{i}_cropped.mp4"]
    subprocess.run(command1)

    command2 = ['ffmpeg', '-y', '-i', f"{subway_folder}/subway_clip{i}.mp4", '-vf', 'crop=w=iw-250:h=ih:x=100:y=0',
                f"{subway_folder}/subway_clip{i}_cropped.mp4"]
    subprocess.run(command2)

    video1 = VideoFileClip(f"{shorts_folder}/clip{i}_cropped.mp4")
    video2 = VideoFileClip(f"{subway_folder}/subway_clip{i}_cropped.mp4").without_audio()
    merged_video = clips_array([[video1], [video2]])
    merged_video.write_videofile(f"{shorts_merged_folder}/merged_video{i}.mp4", codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)


    file = f"./{shorts_folder}/clip{i}.mp4"
    subs_ai = SubsAI()
    model = subs_ai.create_model('openai/whisper', {'model_type': 'medium'})
    subs = subs_ai.transcribe(file, model)
    subs.save(f"{shorts_sub_folder}/clip{i}sub.srt")
    command = [
        'ffmpeg', '-y', '-i', f"{shorts_merged_folder}/merged_video{i}.mp4",
        '-vf', f"subtitles={shorts_sub_folder}/clip{i}sub.srt:force_style='Alignment=2'",
        f"{shorts_done_folder}/clip{i}DONE.mp4"
    ]
    subprocess.run(command)


