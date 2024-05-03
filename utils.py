import cv2
import numpy as np


def image_watermark(img, img_watermark, scale=3):
    img_wm_h, img_wm_w = img_watermark.shape[:2]
    img_wm_h_resize, img_wm_w_resize = int(img_wm_h / scale), int(img_wm_w / scale)
    img_watermark_resize = cv2.resize(img_watermark, (img_wm_w_resize, img_wm_h_resize),
                                      interpolation=cv2.INTER_CUBIC)
    img_wm_alpha = img_watermark_resize[:, :, 3].copy()
    img_watermark_resize[:, :, 3:] = img_watermark_resize[:, :, 3:] * 0.6
    img[-img_wm_h_resize:, :img_wm_w_resize][img_wm_alpha > 127] = img_watermark_resize[img_wm_alpha > 127]
    return img
