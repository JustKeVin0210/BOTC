import os
import json
from collections import defaultdict


def add_jinx_json(json_file, jinx_file, save_path):
    with open(json_file, "r", encoding='utf-8') as f:
        json_data = json.load(f)
    with open(jinx_file, "r", encoding='utf-8') as f:
        jinx_data = json.load(f)
        if jinx_data[0].get("id") == "_meta":
            jinx_data.pop(0)
    jinx_index_dict = defaultdict(list)
    for i, jinx_info in enumerate(jinx_data):
        jinx_role1, jinx_role2 = jinx_info.get("id").split("+")
        jinx_index_dict[jinx_role1 + "TRANS"].append((i, jinx_role2 + "TRANS"))
    for json_info in json_data:
        if json_info.get("id") == "_meta":
            continue
        role_id = json_info.get("id") + ""
        jinx_list = []
        for jinx_index, jinx_role in jinx_index_dict.get(role_id, []):
            jinx_dict = defaultdict()
            jinx_dict["id"] = jinx_role
            jinx_dict["reason"] = jinx_data[jinx_index]["ability"]
            jinx_list.append(jinx_dict)
        if jinx_list:
            json_info["jinxes"] = jinx_list
        else:
            json_info.pop("jinxes", None)
    new_json_name = os.path.basename(json_file).replace(".json", "_jinx.json")
    with open(os.path.join(save_path, new_json_name), "w", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"{os.path.basename(json_file)}添加冲突规则完成")
    return


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
    json_file = r"json/全角色.json"
    jinx_file = r"json/冲突规则_水印.json"
    save_path = r"json"
    add_jinx_json(json_file, jinx_file, save_path)

    json_file = r"json/全角色_hr.json"
    jinx_file = r"json/冲突规则_水印.json"
    save_path = r"json"
    add_jinx_json(json_file, jinx_file, save_path)

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
