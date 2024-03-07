import os
import random

def rename_images():
    # 対象のフォルダパス
    folder_path = 'image'

    # フォルダ内の画像ファイルのリストを取得
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # ファイルをランダムな名前にリネーム
    for image_file in image_files:
        # 新しいランダムなファイル名を生成
        random_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8)) + os.path.splitext(image_file)[1]

        # ファイルの移動とリネーム
        os.rename(os.path.join(folder_path, image_file), os.path.join(folder_path, random_name))
        print(f'Renamed {image_file} to {random_name}')

    # フォルダ内の画像ファイルのリストを再度取得
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # 画像ファイルを連番でリネーム
    for i, image_file in enumerate(image_files):
        # 新しいファイル名を生成
        new_filename = f'{i+1}.png'  # 3桁の連番でリネームする場合の例

        # ファイルの移動とリネーム
        os.rename(os.path.join(folder_path, image_file), os.path.join(folder_path, new_filename))
        print(f'Renamed {image_file} to {new_filename}')

