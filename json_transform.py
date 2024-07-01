import os
import json
from bisect import bisect_left


def transform_json(origin_json_file, all_role_json_file, save_path, logo_url=""):
    with open(origin_json_file, "r", encoding='utf-8') as f:
        origin_json = json.load(f)
    with open(all_role_json_file, "r", encoding='utf-8') as f:
        all_role_json = json.load(f)
    tf_json = [
        {
            "id": "_meta",
            "name": f"{os.path.basename(origin_json_file).split('.')[0]}",
            "a jinxed": "相克规则",
            "a role": "衍生角色"
        }
    ]
    if all_role_json[0].get("id") == "_meta":
        all_role_json.pop(0)
    all_role_json = sorted(all_role_json, key=lambda x: x.get("id"))
    all_role_id = [role.get("id") for role in all_role_json]
    if logo_url:
        tf_json[0]["logo"] = logo_url
    for role_info in origin_json:
        assert role_info.get("id")
        index = bisect_left(all_role_id, role_info.get("id") + "TRANS")
        assert all_role_json[index].get("id") == role_info.get("id") + "TRANS"
        tf_json.append(all_role_json[index])
    new_json_name = os.path.basename(origin_json_file).replace(".json", "_tf.json")
    with open(os.path.join(save_path, new_json_name), "w", encoding='utf-8') as f:
        json.dump(tf_json, f, ensure_ascii=False, indent=2)
    print(f"json文件已经保存到{new_json_name}")
    return


if __name__ == '__main__':
    origin_json_file = r"json_script/长夜险恶.json"
    all_role_json_file = r"json/全角色_hr.json"
    save_path = r"./json"
    logo_url = r"https://i.postimg.cc/GtZVBcXQ/image.png"
    transform_json(origin_json_file, all_role_json_file, save_path, logo_url=logo_url)
