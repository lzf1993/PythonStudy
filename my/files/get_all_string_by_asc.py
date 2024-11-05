import struct
import sys


def read_string(pool, index):
    # 从字符串池中获取字符串
    length = pool[index * 4 + 2]
    offset = pool[index * 4 + 3]
    return pool[offset:offset + length].decode('utf-8')


def parse_resources_arsc(file_path):
    with open(file_path, 'rb') as f:
        # 读取头部
        header = f.read(4)
        if header != b'\x00\x00\x00\x01':
            print("Not a valid resources.arsc file.")
            return

        # 读取资源数量
        f.seek(16)  # 偏移到资源数量的位置
        resource_count = struct.unpack('<I', f.read(4))[0]

        # 读取字符串池
        f.seek(28)  # 偏移到字符串池的位置
        string_pool_size = struct.unpack('<I', f.read(4))[0]
        f.seek(32)  # 偏移到字符串数据
        string_pool = f.read(string_pool_size)

        strings = []
        for i in range(resource_count):
            string = read_string(string_pool, i)
            strings.append(string)

        return strings


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_arsc.py <path_to_resources.arsc>")
        sys.exit(1)

    file_path = sys.argv[1]
    strings = parse_resources_arsc(file_path)

    if strings:
        print("Extracted Strings:")
        for s in strings:
            print(s)
