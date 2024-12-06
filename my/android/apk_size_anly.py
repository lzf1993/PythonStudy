import sqlite3

from androguard.core.axml import ARSCParser
from androguard.core.apk import APK


def extract_apk_info(apk_file):
    apk = APK(apk_file)
    file_types = {}
    for file in apk.get_files():
        file_type = file.split('.')[-1]  # 获取文件类型
        file_size = file
        if file_type in file_types:
            file_types[file_type] += file_size
        else:
            file_types[file_type] = file_size
    return file_types


# 创建 表信息
def create_database(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS apk_info
                 (file_type TEXT, size INTEGER)''')
    conn.commit()
    conn.close()



# 插入 apk 信息
def insert_apk_info(db_file, apk_info):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for file_type, size in apk_info.items():
        c.execute("INSERT INTO apk_info (file_type, size) VALUES (?, ?)", (file_type, size))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    apk_file = '/Users/lzf2/Downloads/4720009_us_20241105.apk'
    db_file = 'your_database.db'

    apk_info = extract_apk_info(apk_file)
    create_database(db_file)
    insert_apk_info(db_file, apk_info)
