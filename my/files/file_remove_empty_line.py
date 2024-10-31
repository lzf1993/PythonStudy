


def remove_empty_lines(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # 过滤掉空行
    non_empty_lines = [line for line in lines if line.strip() != '']

    with open(output_file, 'w') as file:
        file.writelines(non_empty_lines)


if __name__ == '__main__':
    # 使用示例
    file_out_path = 'record_new.txt'
    file_int_path = 'record.txt'
    remove_empty_lines(file_int_path, file_out_path)


