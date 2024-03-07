import cv2
import numpy as np
import os
from moviepy.editor import *

def create_video(image_dir, audio_dir, output_dir, output_name, video_width, video_height):
    # 画像と音声のファイルリストを取得し、連番順にソートする
    image_files = sorted([f for f in os.listdir(image_dir) if f.endswith('.png')], key=lambda x: int(x.split('.')[0]))
    audio_files = sorted([f for f in os.listdir(audio_dir) if f.endswith('.wav')], key=lambda x: int(x.split('.')[0]))

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 画像と音声の組み合わせを作成して動画を作成
    clips = []
    for idx, (image_file, audio_file) in enumerate(zip(image_files, audio_files)):
        # 画像と音声のパスを取得
        image_path = os.path.join(image_dir, image_file)
        audio_path = os.path.join(audio_dir, audio_file)

        # 画像を読み込み（BGRからRGBに変換）
        frame = cv2.imread(image_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 最初の画像だけ少し下にずらす
        if idx == 0:
            shift_pixels = 450  # ずらすピクセル数を設定
            frame = np.roll(frame, shift_pixels, axis=0)
            frame[:shift_pixels, :] = 0  # ずらした部分を黒く塗りつぶす

        # 画像を指定したサイズにリサイズ
        frame = cv2.resize(frame, (video_width, video_height))

        # 画像クリップを作成
        image_clip = ImageClip(frame, duration=1)  # 1秒間表示されるクリップを作成

        # 音声クリップを作成
        audio_clip = AudioFileClip(audio_path)

        # 音声クリップの長さを取得して画像クリップに合わせる
        duration = audio_clip.duration

        # 画像クリップと音声クリップを合成してクリップを作成
        clip = CompositeVideoClip([image_clip.set_duration(duration).set_audio(audio_clip)])

        clips.append(clip)

    # すべてのクリップを連結してビデオを作成
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # FPSを設定
    final_clip.fps = 24

    # ビデオを出力
    final_clip.write_videofile(os.path.join(output_dir, output_name + '.mp4'), codec='libx264', audio_codec='aac', bitrate='160k', threads=4)
