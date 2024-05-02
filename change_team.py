import cv2
import numpy as np
import os

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


def change_color_team(img_folder, save_folder):
    if not os.path.exists(img_folder):
        raise Exception(f"{img_folder}文件夹缺失，请执行img_download.py生成")
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
        cv2.imwrite(os.path.join(save_folder, img_name), img)
        print(f"{os.path.basename(img_name)}阵营转换后图片处理完成")


def change_color(img_origin_folder, save_path):
    role_team_list = ["townsfolk", "outsider", "minion", "demon"]
    for role_team in role_team_list:
        img_folder = os.path.join(img_origin_folder, "origin", role_team)
        save_folder = os.path.join(save_path, "change_team", role_team)
        os.makedirs(save_folder, exist_ok=True)
        change_color_team(img_folder, save_folder)


if __name__ == '__main__':
    img_origin_folder = r"./image"
    save_path = r"./image"
    change_color(img_origin_folder, save_path)

