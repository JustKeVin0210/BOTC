import os
import numpy as np
import cv2
import json


def merge_image(img_base_bgr, img_base_alpha, img_1, img_2):
    img_h_1, img_w_1 = img_1.shape[:2]
    img_h_2, img_w_2 = img_2.shape[:2]
    img_h, img_w = min(img_h_1, img_h_2), min(img_w_1, img_w_2)
    img_base_zeros = np.zeros((img_h * 2, img_w * 2, 4), dtype=np.uint8)
    if img_base_bgr is not None and img_base_alpha is not None:
        img_base_h, img_base_w = img_base_bgr.shape[:2]
        h_start, w_start = (img_h * 2 - img_base_h) // 2, (img_w * 2 - img_base_w) // 2
        h_end, w_end = h_start + img_base_h, w_start + img_base_w
        img_base_zeros[h_start:h_end, w_start:w_end] = np.concatenate((img_base_bgr, img_base_alpha), axis=-1)
    img_out = np.zeros((img_h * 2, img_w * 2, 4), dtype=np.uint8)
    img_resize_1 = cv2.resize(img_1, (img_w, img_h), interpolation=cv2.INTER_CUBIC)
    img_resize_2 = cv2.resize(img_2, (img_w, img_h), interpolation=cv2.INTER_CUBIC)
    img_out[:img_h, :img_w] = img_resize_1
    img_out[-img_h:, -img_w:] = img_resize_2
    img_out[img_base_zeros[:, :, 3] > 127] = img_base_zeros[img_base_zeros[:, :, 3] > 127]
    return img_out


def jinx(img_origin_folder, save_path, jinx_json):
    img_base_dir = os.path.join(img_origin_folder, "jinx", "jinx.png")
    save_folder = os.path.join(save_path, "jinx")
    os.makedirs(save_folder, exist_ok=True)
    if not os.path.exists(img_base_dir):
        img_base_bgr, img_base_alpha = None, None
    else:
        img_base = cv2.imread(img_base_dir, -1)
        img_base_bgr, img_base_alpha = img_base[:, :, :3], img_base[:, :, 3:]
    with open(jinx_json, "r", encoding='utf-8') as f:
        jinx_info_list = json.load(f)
    if jinx_info_list[0].get("id") == "_meta":
        jinx_info_list.pop(0)
    for jinx_info in jinx_info_list:
        jinx_names = jinx_info.get("id").split("+")
        img_jinx_name = f"{jinx_names[0]}_{jinx_names[1]}.png"
        jinx_name_1, jinx_name_2 = map(lambda x: os.path.join(img_origin_folder, x.capitalize() + ".png"), jinx_names)
        assert os.path.exists(jinx_name_1), f"{os.path.basename(jinx_name_1)}图片不存在"
        assert os.path.exists(jinx_name_2), f"{os.path.basename(jinx_name_2)}图片不存在"
        img_1 = cv2.imread(jinx_name_1, -1)
        img_2 = cv2.imread(jinx_name_2, -1)
        img_out = merge_image(img_base_bgr, img_base_alpha, img_1, img_2)
        cv2.imwrite(os.path.join(save_folder, img_jinx_name), img_out)
        print(f"{img_jinx_name}图片处理完成")
    return


if __name__ == '__main__':
    img_origin_folder = r"./image_all"
    save_path = r"./image"
    jinx_json = r"./冲突规则.json"
    jinx(img_origin_folder, save_path, jinx_json)
