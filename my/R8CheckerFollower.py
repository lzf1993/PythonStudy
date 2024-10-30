#!/usr/bin/python3
import json

prePath = "/Users/lzf2/Documents/weipai/wejoy_ar/wejoy/"
allClassMapFile = prePath + "annotation_map.json"
suspiciousClassFile = prePath + "suspicious_class_set.json"
java_inner_class = ["I", "F", "D", "J", "Z", "java/lang/String", "java/lang/Object"]

visited_classes = dict()

check = 0
check_field = 0


def read_from_json(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    return data


def get_class_from_str(v: str) -> str:
    if v == "I":
        return "int"
    if v == "F":
        return "float"
    if v == "D":
        return "double"
    if v == "J":
        return "long"
    if v == "Z":
        return "boolean"
    if v.startswith("["):
        return get_class_from_str(v[1:])
    if v.startswith("L") and v.endswith(";"):
        return v[1:-1]
    return v


def find_class_field_with_out_serializable(all_class_map: dict, clazz: str, super_class: str = None):
    if visited_classes.__contains__(clazz):
        return
    visited_classes[clazz] = True
    if clazz in java_inner_class:
        return
    if clazz.startswith("java."):
        return
    # [(clazz, bool)]
    clazz_and_field = all_class_map.get(clazz)
    if clazz_and_field is None:
        print(f"\033[91m[404 Not Found]{clazz}\033[0m")
        return
    to_do_check = []
    first = True
    for (varName, extra) in clazz_and_field.items():
        if varName.startswith("this$"):
            # inner class maybe?
            continue
        ann = extra['first']
        raw_type = extra['second']
        field_type = get_class_from_str(raw_type).replace('/', '.')
        if not ann:
            global check_field
            check_field += 1
            if first:
                print(f"\033[1m{clazz}{' <- ' if super_class else ''}{super_class}\033[0m")
                global check
                check += 1
                first = False
            c = f"public {field_type} "
            print(f"\033[94m| \033[0m {c}{varName}")
            print(
                f"\033[94m| \033[0m \033[91m\033[1m{' ' * len(c)}{'~' * len(varName)} missing @SerializedName?\033[0m")
        if raw_type not in java_inner_class and not raw_type.startswith("java/") and not raw_type.startswith("Ljava/"):
            to_do_check.append(field_type)
    for c in to_do_check:
        find_class_field_with_out_serializable(all_class_map, c, clazz)


if __name__ == "__main__":
    # clazz:[(clazz, bool)]
    allClassMap = read_from_json(allClassMapFile)
    type_class = read_from_json(suspiciousClassFile)
    print(f"Found {len(type_class)} classes.")
    for c in type_class:
        find_class_field_with_out_serializable(allClassMap, c.replace("/", "."))
    print(f"Total {check} files ({check_field} fields) need to be checked.")
