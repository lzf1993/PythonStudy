

## 查找 文件 A 在 文件 B 中存在的内容，并写入到文件 C
def find_exit_content(fila_a, file_b, file_c):
    # 读取文件 B 的内容，存入一个集合中（为了提高查找效率）
    with open(file_b, 'r', encoding='utf-8') as f_b:
        b_content = set(f_b.read().splitlines())  # 将文件 B 的每一行作为集合中的一个元素

    # 打开文件 C，准备写入符合条件的行
    with open(file_c, 'w', encoding='utf-8') as f_c:
        with open(file_a, 'r', encoding='utf-8') as f_a:
            for line in f_a:
                line = line.strip()  # 去除每行末尾的换行符和空格
                if line in b_content:  # 如果文件 A 的行在文件 B 中存在
                    f_c.write(line + '\n')  # 将符合条件的行写入到文件 C

    print(f"匹配的内容已经写入到 {file_c}")


if __name__ == '__main__':

    # 读取文件 A 和文件 B
    file_a = '../android/temp/clear_string_record.txt'  # 文件 A 路径
    file_b = '../android/temp/android_strings_output.txt'  # 文件 B 路径
    file_c = '../android/temp/file_C.txt'  # 文件 C 路径

    find_exit_content(file_a, file_b, file_c)

