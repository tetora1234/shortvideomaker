from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import moviepy.config

def add_subtitles_to_video(input_video_path, output_video_path, subtitles):
    # ImageMagickのバイナリパスを設定
    moviepy.config.change_settings({"IMAGEMAGICK_BINARY": r"C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})
    
    # 動画の読み込み
    video_clip = VideoFileClip(input_video_path)

    # 字幕用のクリップを作成
    subtitles_clips = [TextClip(txt, fontsize=96, color='white', font='C:/Windows/Fonts/meiryob.ttc',
                                stroke_color='#FFA500', stroke_width=3, method='caption', kerning=-1, size=(1080, 1920))  # 縁取りの設定
                       .set_position(('center', 100))
                       .set_start(start)  # ここで字幕の開始時間を設定
                       .set_duration(end - start)
                       for start, end, txt in subtitles]

    # 上部に白い背景色を持つテキストクリップを作成
    first_subtitle_clip = TextClip(subtitles[0][2], fontsize=96, color='white', bg_color='#808080', font='C:/Windows/Fonts/meiryob.ttc',
                                   stroke_color='black', stroke_width=3, method='caption', kerning=-1, size=(1080, 450))  # サイズを調整
    first_subtitle_clip = first_subtitle_clip.set_position(('center', 0)).set_start(subtitles[0][0]).set_duration(subtitles[0][1] - subtitles[0][0])

    # 字幕を重ねて新しい動画を作成
    final_clip = CompositeVideoClip([video_clip, first_subtitle_clip] + subtitles_clips[1:], size=video_clip.size)

    # 動画を保存
    final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac')