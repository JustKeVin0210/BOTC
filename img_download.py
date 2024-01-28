import os
import time
import requests
import json


def download_image(image_dir, json_file):
    os.makedirs(image_dir, exist_ok=True)
    with open(json_file, "r", encoding='utf-8') as f:
        script_roles = json.load(f)
    for role_info in script_roles:
        url = role_info.get("image")
        name = role_info.get("name")
        chunk_download(image_dir, url, name)


def chunk_download(image_dir, image_url, name):
    r = requests.get(image_url, stream=True)
    t0 = time.time()
    # with open(os.path.join(image_dir, name + ".png"), 'wb') as f:
    #     f.write(r.content)
    with open(os.path.join(image_dir, name + ".png"), 'wb') as f:
        for chunk in r.iter_content(chunk_size=32):
            f.write(chunk)

    t = time.time()
    print("{}图标已经下载完成，用时{}s".format(name, t - t0))


if __name__ == '__main__':
    save_path = r"./image"
    js_file = r"./全角色.json"
    download_image(save_path, js_file)
