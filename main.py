import requests
from delete import delete_folder_contents
from renban import rename_images
import voicepeak
import srtmake
import videomake
import subtitling
import srtread
import os
import time
from bs4 import BeautifulSoup

# 画像の並びをリセットして作成ごとに違う画像を使うようにする
rename_images()
# 前回作成したデータを削除してから開始
delete_folder_contents('output')
delete_folder_contents('voice')

# スクレイピング対象のURL
url = 'https://mi.5ch.net/test/read.cgi/news4vip/1709653285/'
title = 'ブルアカのゲーム開発部えっろｗｗｗ\nスレ反応集'

# URLからHTMLを取得
response = requests.get(url)
html = response.text

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(html, 'html.parser')

# テキスト抽出
save_path = "C:/Users/nider/Desktop/git/shortvideosmaker/voice"
file_name = os.path.join(save_path, f'1.txt')
with open(file_name, 'w', encoding='utf-8') as file:
    file.write(title)
voicepeak.makeVoicePeak(title, 1)

articles = soup.find_all('section', class_='post-content')

# 開始インデックスと抽出する記事の数を定義します
start_index = 1  # 例えば、3番目の記事から開始します
num_articles = 1  # 例えば、5つの記事を抽出します

counter = 2
idx = start_index
# NGワードリスト
ng_words = ["嫌儲", "殺", "ネトウヨ", ">>"]

while idx < len(articles) and counter-1 <= num_articles:
    article = articles[idx]
    article_text = article.text.strip()  # 記事のテキストを取得し、前後の空白を削除します

    # 指定した文字数以下の場合はスキップします
    if len(article_text) > 30:  
        print(f"Article {idx} is too short, skipping...")
        idx += 1
        continue
    # NGワードが含まれている場合はスキップします
    if any(word in article_text for word in ng_words):
        print(f"Article {idx} contains NG word, skipping...")
        idx += 1
        continue

    print(f'{counter-1} {article_text}')
    file_name = os.path.join(save_path, f'{counter}.txt')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(article_text)
    voicepeak.makeVoicePeak(article_text, counter)
    time.sleep(0.5)
    counter += 1
    idx += 1

videomake.create_video(
    image_dir=r'C:/Users/nider/Desktop/git/shortvideosmaker/image',
    audio_dir=r'C:/Users/nider/Desktop/git/shortvideosmaker/voice',
    output_dir=r'C:/Users/nider/Desktop/git/shortvideosmaker/output',
    output_name=r'C:/Users/nider/Desktop/git/shortvideosmaker/output/video',
    video_width=1080,
    video_height=1920
)

srtmake.make_srt_file('voice', "C:/Users/nider/Desktop/git/shortvideosmaker/output", 'output.srt')

input_video_path = "C:/Users/nider/Desktop/git/shortvideosmaker/output/video.mp4"
output_video_path = "C:/Users/nider/Desktop/git/shortvideosmaker/output/videos_srt_add.mp4"
srt_file_path = "C:/Users/nider/Desktop/git/shortvideosmaker/output/output.srt"
subtitles = srtread.read_srt_file(srt_file_path)

subtitling.add_subtitles_to_video(input_video_path, output_video_path, subtitles)
