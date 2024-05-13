import os
import json


def merge_json(json_list, json_save_path):
    data_list = []
    name_list = []
    for i, json_file in enumerate(json_list):
        assert os.path.exists(json_file), f"{json_file}文件不存在"
        with open(json_file, "r", encoding='utf-8') as f:
            json_data = json.load(f)
        if i > 0 and json_data[0].get("id") == "_meta":
            json_data.pop(0)
        data_list.extend(json_data)
        name_list.append(os.path.basename(json_file).split(".")[0])
    json_name = "_".join(name_list) + ".json"
    json_save_file = os.path.join(json_save_path, json_name)
    with open(json_save_file, "w", encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
    print(f"json文件{json_name}合并完成")


if __name__ == '__main__':
    json_list = [
        r"json/全角色.json",
        r"json/冲突规则_水印.json"
    ]
    json_save_path = r"json"
    merge_json(json_list, json_save_path)

    json_list = [
        r"json/全角色.json",
        r"json/冲突规则.json"
    ]
    json_save_path = r"json"
    merge_json(json_list, json_save_path)

    json_list = [
        r"json/全角色_hr.json",
        r"json/冲突规则_水印.json"
    ]
    json_save_path = r"json"
    merge_json(json_list, json_save_path)

    json_list = [
        r"json/全角色_hr.json",
        r"json/冲突规则.json"
    ]
    json_save_path = r"json"
    merge_json(json_list, json_save_path)
