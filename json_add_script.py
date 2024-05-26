import os
import json
import requests
from bs4 import BeautifulSoup

URL = "https://clocktower-wiki.gstonegames.com/index.php?"


def get_script_dict(origin_json_file):
    with open(origin_json_file, "r", encoding='utf-8') as f:
        origin_json = json.load(f)
    if origin_json[0].get("id") == "_meta":
        origin_json.pop(0)
    script_dict = {}
    print(len(origin_json))
    for i, role_info in enumerate(origin_json):
        script = role_info.get("name")
        if role_info.get("team") == "fabled" :
            script_dict[script] = "传奇角色"
            continue
        if i < 27:
            script_dict[script] = "暗流涌动"
        elif 27 <= i < 27 + 30:
            script_dict[script] = "黯月初升"
        elif 27 + 30 <= i < 27 + 30 + 30:
            script_dict[script] = "梦殒春宵"
        elif 27 + 30 + 30 + 55 <= i < 27 + 30 + 30 + 55 + 27:
            script_dict[script] = "华灯初上"
        else:
            script_dict[script] = "实验性角色"
    json.dump(script_dict, open("json/script_dict.json", "w", encoding='utf-8'), ensure_ascii=False, indent=2)
    return script_dict


def add_script(origin_json_file, script_json_file, save_path):
    # get_script_dict(origin_json_file)
    with open(origin_json_file, "r", encoding='utf-8') as f:
        origin_json = json.load(f)
    if origin_json[0].get("id") == "_meta":
        origin_json.pop(0)
    with open(script_json_file, "r", encoding='utf-8') as f:
        script_dict = json.load(f)
    assert len(origin_json) == len(script_dict)
    for role_info, role_script in zip(origin_json, script_dict.items()):
        assert role_info["name"] == role_script[0]
        role_info["script"] = role_script[1]
    new_json_name = os.path.basename(origin_json_file).replace(".json", "_script.json")
    json.dump(origin_json, open(os.path.join(save_path, new_json_name), "w", encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(origin_json_file)}剧本添加完成")
    return


if __name__ == '__main__':
    origin_json_file = r"json/全角色.json"
    script_json_file = r"json/script_dict.json"
    save_path = r"./json"
    add_script(origin_json_file, script_json_file, save_path)
