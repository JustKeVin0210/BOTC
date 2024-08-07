import cv2
import numpy as np
import os
from utils import image_watermark

H_MEAN_BLUE = 100
H_MEAN_RED = 5


def change_color_blue2red(img, h_value=H_MEAN_RED):
    img_bgr, img_alpha = img[:, :, :3], img[:, :, 3:]
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_hsv = img_hsv.astype(np.float32)
    img_hsv[:, :, 0:1] = h_value
    img_hsv = np.clip(img_hsv, 0, 255)
    img_hsv = img_hsv.astype(np.uint8)
    img_bgr_new = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return np.concatenate((img_bgr_new, img_alpha), axis=-1)


def change_color_red2blue(img, h_value=H_MEAN_BLUE):
    img_bgr, img_alpha = img[:, :, :3], img[:, :, 3:]
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_hsv = img_hsv.astype(np.float32)
    img_hsv[:, :, 0:1] = h_value
    img_hsv = np.clip(img_hsv, 0, 255)
    img_hsv = img_hsv.astype(np.uint8)
    img_bgr_new = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    return np.concatenate((img_bgr_new, img_alpha), axis=-1)


def change_color_team(img_folder, save_folder, watermark=""):
    assert os.path.exists(img_folder), f"{img_folder}文件夹缺失，请执行img_download.py生成"
    base_name = os.path.basename(img_folder)
    img_name_list = [i for i in sorted(os.listdir(img_folder)) if i.endswith(".png")]
    for img_name in img_name_list:
        img_dir = os.path.join(img_folder, img_name)
        img = cv2.imread(img_dir, -1)
        if base_name in ["townsfolk", "outsider"]:
            img = change_color_blue2red(img)
        elif base_name in ["minion", "demon"]:
            img = change_color_red2blue(img)
        else:
            pass
        if os.path.exists(watermark):
            img = image_watermark(img, cv2.imread(watermark, -1))
        if not os.path.exists(os.path.join(save_folder, img_name)):
            cv2.imwrite(os.path.join(save_folder, img_name), img)
            save_folder_new = os.path.join(save_folder.split("change_team")[0], "change_team_new")
            os.makedirs(save_folder_new, exist_ok=True)
            cv2.imwrite(os.path.join(save_folder_new, img_name), img)
            print(f"{img_name}阵营转换后图片处理完成")
        else:
            print(f"{img_name}阵营转换后图片已存在")


def change_color(img_origin_folder, save_path, watermark=""):
    if os.path.exists(watermark):
        save_path = save_path + "_watermark"
    role_team_list = ["townsfolk", "outsider", "minion", "demon"]
    for role_team in role_team_list:
        img_folder = os.path.join(img_origin_folder, "origin", role_team)
        save_folder = os.path.join(save_path, "change_team", role_team)
        os.makedirs(save_folder, exist_ok=True)
        change_color_team(img_folder, save_folder, watermark=watermark)


if __name__ == '__main__':
    img_origin_folder = r"./image"
    save_path = r"./image"
    watermark = r"./image_all/watermark/Just_KeVin.png"
    change_color(img_origin_folder, save_path, watermark=watermark)

    change_color(img_origin_folder, save_path)
