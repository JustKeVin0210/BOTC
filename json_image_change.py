import json
import os

wrong_image = {
    "villageidiot": "https://wiki.bloodontheclocktower.com/images/d/da/Icon_villageidiot.png",
    # "villageidiot": "https://oss.gstonegames.com/data_file/clocktower/web/icons/villageidiot.png",
    "zealot": "https://wiki.bloodontheclocktower.com/images/1/16/Icon_zealot.png",
    # "zealot": "https://oss.gstonegames.com/data_file/clocktower/web/icons/zealot.png",
}


def image_change(origin_json_file, save_path):
    with open(origin_json_file, "r", encoding='utf-8') as f:
        origin_json = json.load(f)
    for role_info in origin_json:
        if role_info.get("id") == "_meta":
            continue
        if role_info.get("team") in ["townsfolk", "outsider", "minion", "demon", "traveler"]:
            role_id = role_info.get("id").replace("TRANS", "")
            if role_id in wrong_image.keys():
                role_info["image"] = wrong_image[role_id]
            else:
                role_info["image"] = f"https://oss.gstonegames.com/data_file/clocktower/web/icons/{role_id}.png"
    new_json_name = os.path.basename(origin_json_file).replace(".json", "_hr.json")
    with open(os.path.join(save_path, new_json_name), "w", encoding='utf-8') as f:
        json.dump(origin_json, f, ensure_ascii=False, indent=2)
    print(f"{os.path.basename(origin_json_file)}图片修改完成")
    return


if __name__ == '__main__':
    origin_json_file = r"json/全角色.json"
    save_path = r"./json"
    image_change(origin_json_file, save_path)
