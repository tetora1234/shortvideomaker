import wave
import glob
import textwrap
from typing import NamedTuple
from datetime import timedelta
import os

class SrtInfo(NamedTuple):
    num: int
    start: str
    end: str
    text: str


def make_srt_file(folder: str, output_folder: str, filename: str) -> None:
    txtfiles = get_txt_files(folder)
    wavfiles = get_wav_files(folder)
    output_path = os.path.join(output_folder, filename)
    # SubRipファイルの初期化
    with open(output_path, mode='w') as f:
        f.write('')
    srtinfo_list = make_srtinfo_list(txtfiles, wavfiles)
    for srtinfo in srtinfo_list:
        write_srttime(srtinfo, output_path)



def get_txt_files(folder: str) -> list:
    return sorted(glob.glob(f'{folder}/*.txt'))


def get_wav_files(folder: str) -> list:
    return sorted(glob.glob(f'{folder}/*.wav'))


def make_srtinfo_list(txtfiles: list, wavfiles: list) -> list:
    """SubRipファイルに必要な情報をまとめたSrtInfoのリストをつくる"""
    basetime = timedelta(0, 0, 0)
    srtinfo_list = []
    # 連番順にソート
    txtfiles = sorted(txtfiles, key=lambda x: int(os.path.basename(x).split('.')[0]))
    wavfiles = sorted(wavfiles, key=lambda x: int(os.path.basename(x).split('.')[0]))
    for i, (t, w) in enumerate(zip(txtfiles, wavfiles)):
        text = get_text(t)
        start = format_srttime(basetime)
        playtime = calc_playtime(w)
        # 若干時間を削ったほうが整合する｡丸め誤差の影響か？
        playtime -= 0.017
        basetime = basetime + timedelta(seconds=playtime)
        end = format_srttime(basetime)
        srtinfo = SrtInfo(i+1, start, end, text)
        srtinfo_list.append(srtinfo)
    return srtinfo_list



def get_text(txt_file: str) -> str:
    with open(txt_file, mode='r', encoding='utf-8') as f:
        text =  f.read()
    # 一行あたりの文字数が300あたりを超えるとPremiere Proがエラーを起こすので改行を挟む
    return textwrap.fill(text, 200)


def format_srttime(timedelta: timedelta) -> str:
    """timedeltaをSubRip形式の時間表示にフォーマットする"""
    ss, mi = divmod(timedelta.total_seconds(), 1)
    mi = int(round(mi, 3)*1000)
    mm, ss = divmod(ss, 60)
    hh, mm = divmod(mm, 60)
    srttime = f'{int(hh):02}:{int(mm):02}:{int(ss):02},{mi:03}'
    return srttime


def calc_playtime(wav_file: str) -> float:
    """waveファイルのフレームレートとフレーム数から再生時間を計算する"""
    with wave.open(wav_file, mode='rb') as wr:
        fr = wr.getframerate()
        fn = wr.getnframes()
        playtime = fn/fr
        return playtime


def write_srttime(srt: SrtInfo, filename: str) -> None:
    """SrtInfoを受け取ってSubRipファイルに必要な情報を順次加筆していく"""
    with open(filename, mode='a', encoding='utf-8') as f:  # 追記: encoding='utf-8'
        srt_items = [
            str(srt.num)+'\n',
            f'{srt.start} --> {srt.end}\n',
            srt.text+'\n\n'
            ]
        f.writelines(srt_items)