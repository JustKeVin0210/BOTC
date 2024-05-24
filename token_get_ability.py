import os
import numpy as np
import cv2
from utils import image_watermark


role_path_list = [
    {
        "id": "Drunk",
        "real_role_path": "origin/outsider/Drunk.png",
        "ability_role_path_list": ["origin/townsfolk"],
    },
    {
        "id": "Lunatic",
        "real_role_path": "origin/outsider/Lunatic.png",
        "ability_role_path_list": ["change_team/demon"],  # "origin/demon",
    },
    {
        "id": "Apprentice",
        "real_role_path": "origin/traveler/Apprentice.png",
        "ability_role_path_list": ["origin/townsfolk", "origin/minion"],
    },
    {
        "id": "Philosopher",
        "real_role_path": "origin/townsfolk/Philosopher.png",
        "ability_role_path_list": ["origin/townsfolk", "origin/outsider"],
    },
    {
        "id": "Alchemist",
        "real_role_path": "origin/townsfolk/Alchemist.png",
        "ability_role_path_list": ["change_team/minion"],  # "origin/minion",
    },
    {
        "id": "Pixie",
        "real_role_path": "origin/townsfolk/Pixie.png",
        "ability_role_path_list": ["origin/townsfolk"],
    },
    {
        "id": "Cannibal",
        "real_role_path": "origin/townsfolk/Cannibal.png",
        "ability_role_path_list": ["origin/townsfolk", "origin/outsider"],
    },
    {
        "id": "Marionette",
        "real_role_path": "origin/minion/Marionette.png",
        "ability_role_path_list": ["change_team/townsfolk", "change_team/outsider"],  # "origin/townsfolk", "origin/outsider"
    },
    {
        "id": "Bianlianshi",
        "real_role_path": "origin/townsfolk/Bianlianshi.png",
        "ability_role_path_list": ["origin/townsfolk", "origin/outsider"],
    },
    {
        "id": "Wudaozhe",
        "real_role_path": "origin/townsfolk/Wudaozhe.png",
        "ability_role_path_list": ["origin/outsider"],
    },
    {
        "id": "Jiaohuazi",
        "real_role_path": "origin/traveler/Jiaohuazi.png",
        "ability_role_path_list": ["origin/townsfolk", "origin/outsider", "origin/minion"],
    },
    {
        "id": "Plague_doctor",
        "real_role_path": "origin/outsider/Plague_doctor.png",
        "ability_role_path_list": ["origin/minion"],
    },
]


def image_merge(img_real, img_ability):
    h_ability, w_ability = img_ability.shape[:2]
    img_real_bgr, img_real_alpha = img_real[:, :, :3], img_real[:, :, 3:]
    img_real_bgr_resize = cv2.resize(img_real_bgr, (w_ability // 2, h_ability // 2), interpolation=cv2.INTER_CUBIC)
    img_real_alpha_resize = cv2.resize(img_real_alpha, (w_ability // 2, h_ability // 2),
                                       interpolation=cv2.INTER_NEAREST)

    img_ability[-h_ability // 2:, -w_ability // 2:, :3][img_real_alpha_resize > 127] = img_real_bgr_resize[
        img_real_alpha_resize > 127]
    img_ability[-h_ability // 2:, -w_ability // 2:, 3:] = np.maximum(
        img_ability[-h_ability // 2:, -w_ability // 2:, 3:],
        img_real_alpha_resize[..., np.newaxis])
    return img_ability


def get_ability_role(img_real_dir, ability_role_folder, save_folder, watermark=""):
    assert os.path.exists(img_real_dir), f"{os.path.basename(img_real_dir)}图片不存在"
    img_real = cv2.imread(img_real_dir, -1)

    img_ability_name_list = [i for i in sorted(os.listdir(ability_role_folder)) if i.endswith(".png")]
    for img_ability_name in img_ability_name_list:
        img_ability_dir = os.path.join(ability_role_folder, img_ability_name)
        assert os.path.exists(img_ability_dir), f"{os.path.basename(img_ability_dir)}图片不存在"
        img_ability = cv2.imread(img_ability_dir, -1)
        img_ability = image_merge(img_real, img_ability)
        img_ability_new_name = f"{os.path.splitext(os.path.basename(img_real_dir))[0]}_{img_ability_name}"
        if os.path.exists(watermark):
            img_ability = image_watermark(img_ability, cv2.imread(watermark, -1))
        if not os.path.exists(os.path.join(save_folder, img_ability_new_name)):
            cv2.imwrite(os.path.join(save_folder, img_ability_new_name), img_ability)
            save_folder_new = os.path.join(save_folder.split("get_ability")[0], "get_ability_new")
            os.makedirs(save_folder_new, exist_ok=True)
            cv2.imwrite(os.path.join(save_folder_new, img_ability_new_name), img_ability)
            print(f"{img_ability_new_name}图片处理完成")
        else:
            print(f"{img_ability_new_name}图片已存在")


def get_ability(img_origin_folder, save_path, role_path_list=role_path_list, watermark=""):
    if os.path.exists(watermark):
        save_path = save_path + "_watermark"
    for role_path in role_path_list:
        img_real_dir = os.path.join(img_origin_folder, role_path["real_role_path"])
        for ability_role_path in role_path["ability_role_path_list"]:
            ability_role_folder = os.path.join(img_origin_folder, ability_role_path)
            save_folder = os.path.join(save_path, "get_ability", role_path["id"], ability_role_path)
            os.makedirs(save_folder, exist_ok=True)
            get_ability_role(img_real_dir, ability_role_folder, save_folder, watermark=watermark)


if __name__ == '__main__':
    img_origin_folder = r"./image"
    save_path = r"./image"
    watermark = r"./image_all/watermark/Just_KeVin.png"
    get_ability(img_origin_folder, save_path, watermark=watermark)

    get_ability(img_origin_folder, save_path)
