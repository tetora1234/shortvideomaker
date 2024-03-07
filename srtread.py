def read_srt_file(srt_file_path):
    subtitles = []
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        index = 0
        while index < len(lines):
            line = lines[index].strip()
            if line.isdigit():
                index += 1
                times = lines[index].strip().split(" --> ")
                start_time = parse_srt_time(times[0])
                end_time = parse_srt_time(times[1])
                index += 1
                subtitle_text = ""
                while index < len(lines) and lines[index].strip() != "":
                    subtitle_text += lines[index].strip() + " "
                    index += 1
                subtitles.append((start_time, end_time, subtitle_text.strip()))
            else:
                index += 1
    return subtitles

def parse_srt_time(srt_time):
    time_parts = srt_time.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds_parts = time_parts[2].split(",")
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
    return total_seconds