from subsai import SubsAI
import os
import subprocess

shorts_folder = "0101"
subway_folder = "subwayserf"
shorts_sub_folder = "0101sub"
os.makedirs(shorts_sub_folder, exist_ok=True)
shorts_done_folder = "0101done"
os.makedirs(shorts_done_folder, exist_ok=True)
counter = len([file for file in os.listdir(shorts_folder) if os.path.isfile(os.path.join(shorts_folder, file))])
for i in range(counter):
    file = f"./{shorts_folder}/clip{i}.mp4"
    subs_ai = SubsAI()
    model = subs_ai.create_model('openai/whisper', {'model_type': 'tiny'})
    subs = subs_ai.transcribe(file, model)
    subs.save(f"{shorts_sub_folder}/clip{i}sub.srt")
    command = ['ffmpeg', '-i', f"{shorts_folder}/clip{i}.mp4", '-vf',
               f"subtitles={shorts_sub_folder}/clip{i}sub.srt", f"{shorts_done_folder}/clip{i}sub.mp4"]
    subprocess.run(command)


    command1 = ['ffmpeg', '-y', '-i', f"{shorts_folder}/clip{i}.mp4", '-vf', 'crop=w=iw-300:h=ih:x=100:y=0',  f"{shorts_folder}/clip{i}_cropped.mp4"]
    subprocess.run(command1)

    command2 = ['ffmpeg', '-y', '-i', f"{subway_folder}/subway_clip{i}.mp4", '-vf', 'crop=w=iw-300:h=ih:x=100:y=0',  f"{subway_folder}/subway_clip{i}_cropped.mp4"]
    subprocess.run(command2)
