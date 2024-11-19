from moviepy.editor import VideoFileClip, clips_array
import os


def merge_videos(video1_path, video2_path, output_path, total_height=720):
    """
    Объединяет два видео: одно сверху (больше на 50 пикселей), другое снизу, исключая аудио нижнего видео, и сохраняет итоговый файл.
    :param video1_path: Путь к первому видео (верхнему).
    :param video2_path: Путь ко второму видео (нижнему).
    :param output_path: Путь для сохранения итогового видео.
    :param total_height: Итоговая высота видео (по умолчанию 770 пикселей, верхнее видео будет больше на 50 пикселей).
    """
    # Загружаем видео
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path).without_audio()  # Убираем аудио из нижнего видео

    # Вычисляем размеры видео
    upper_height = total_height // 2 + 25  # Верхнее видео больше на 50 пикселей
    lower_height = total_height // 2 - 25  # Нижнее видео меньше на 50 пикселей

    # Ресайзим видео
    resized_video1 = video1.resize(height=upper_height)
    resized_video2 = video2.resize(height=lower_height)

    # Объединяем видео одно над другим
    merged_video = clips_array([[resized_video1], [resized_video2]])

    # Сохраняем результат
    merged_video.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True)
    print(f"Объединённое видео сохранено как {output_path}")



# Пример использования
video1_path = "0101done/clip1_sub.mp4"  # Путь к верхнему видео
video2_path = "subwayserf/subway_clip1_cropped.mp4"  # Путь к нижнему видео
output_path = "merged_video.mp4"  # Путь для сохранения результата

merge_videos(video1_path, video2_path, output_path)

# counter_of_shorts = len([file for file in os.listdir(subway_folder) if os.path.isfile(os.path.join(subway_folder, file))])
# for i in range(counter_of_shorts):
#     os.rename(f"{subway_folder}/subway_p{i}.mp4", f"{subway_folder}/clip_p{i}.mp4")