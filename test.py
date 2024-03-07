def filter_file(input_file, output_file, target_string):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            if target_string in line:
                f_out.write(line)

# 使用例
input_file = 'wildcard_character.txt'  # 入力ファイル名
output_file = 'output.txt'  # 出力ファイル名
target_string = 'blue archive'  # フィルターする文字列

filter_file(input_file, output_file, target_string)