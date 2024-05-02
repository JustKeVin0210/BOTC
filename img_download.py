import os
import time
import requests
import json


def chunk_download(image_dir, image_url, role_id):
    r = requests.get(image_url, stream=True)
    t0 = time.time()
    with open(os.path.join(image_dir, role_id + ".png"), 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

    t = time.time()
    print(f"{role_id}图标已经下载完成，用时{t - t0:.6f}s")


def download_image(image_dir, json_file):
    output_dir = os.path.join(image_dir, "origin")
    role_team_list = ["townsfolk", "outsider", "minion", "demon", "traveler", "fabled"]
    for role_team in role_team_list:
        os.makedirs(os.path.join(output_dir, role_team), exist_ok=True)
    with open(json_file, "r", encoding='utf-8') as f:
        script_roles = json.load(f)
    for role_info in script_roles:
        url = role_info.get("image")
        role_id = role_info.get("id").replace("TRANS", "").capitalize()
        role_team = role_info.get("team", "")
        if role_team in role_team_list:
            chunk_download(os.path.join(output_dir, role_team), url, role_id)
        else:
            print(f"{role_id}的角色类型{role_team}为非基本角色类型")


def download_image_cn(image_dir, json_file):
    output_dir = os.path.join(image_dir, "基础角色")
    role_team_cn_dict = {"townsfolk": "镇民", "outsider": "外来者",
                         "minion": "爪牙", "demon": "恶魔",
                         "traveler": "旅行者", "fabled": "传奇角色"}
    for role_team in role_team_cn_dict.values():
        os.makedirs(os.path.join(output_dir, role_team), exist_ok=True)
    with open(json_file, "r", encoding='utf-8') as f:
        script_roles = json.load(f)
    for role_info in script_roles:
        url = role_info.get("image")
        role_name = role_info.get("name")
        role_team = role_team_cn_dict.get(role_info.get("team", ""))
        if role_team in role_team_cn_dict.values():
            chunk_download(os.path.join(output_dir, role_team), url, role_name)
        else:
            print(f"{role_name}的角色类型{role_team}为非基本角色类型")


if __name__ == '__main__':
    save_path = r"./image"
    js_file = r"./全角色.json"
    download_image(save_path, js_file)

    save_path = r"./image_cn"
    js_file = r"./全角色.json"
    download_image_cn(save_path, js_file)
