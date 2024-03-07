import subprocess

def makeVoicePeak(script , filename, narrator = "Japanese Female 1", happy=50, sad=50, angry=50, fun=50):
    """
    任意のテキストをVOICEPEAKのナレーターに読み上げさせる関数
    script: 読み上げるテキスト（文字列）
    narrator: ナレーターの名前（文字列）
    happy: 嬉しさの度合い
    sad: 悲しさの度合い
    angry: 怒りの度合い
    fun: 楽しさの度合い
    """
    # voicepeak.exeのパス
    exepath = "C:/Program Files/VOICEPEAK/voicepeak.exe"
    # wav出力先
    outpath = f"C:/Users/nider/Desktop/git/shortvideosmaker/voice/{filename}.wav"
    # 引数を作成
    args = [
        exepath,
        "-s", script,
        "-n", narrator,
        "-o", outpath,
        "-e", f"happy={happy},sad={sad},angry={angry},fun={fun}"
    ]
    # プロセスを実行
    process = subprocess.Popen(args)

    # プロセスが終了するまで待機
    process.communicate()