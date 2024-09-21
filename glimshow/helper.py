from typing import Tuple, List, Optional
import numpy as np
import numpy.typing as npt
import cv2


def put_text_centered(img, text, font, fontscale, color, thickness):
    textsize = cv2.getTextSize(text, font, fontscale, thickness)[0]
    textX = (img.shape[1] - textsize[0]) / 2
    textY = (img.shape[0] + textsize[1]) / 2
    return cv2.putText(img, text, (int(textX), int(textY)), font, fontscale, color, thickness, cv2.LINE_AA)


def rand_color_image(size: Tuple[int, int], hue: Optional[int] = None, sat: Optional[int] = None, val: Optional[int] = None) -> npt.NDArray[np.uint8]:
    h, w = size

    if hue is None:
        hue = np.random.randint(0, 180)
    if sat is None:
        sat = np.random.randint(0, 255)
    if val is None:
        val = np.random.randint(0, 255)

    color = cv2.cvtColor(np.array([[[hue, sat, val]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)
    img = np.full((h, w, 3), color, dtype=np.uint8)
    return img


def countup_images(size: Tuple[int, int], num: int = 120) -> List[npt.NDArray[np.uint8]]:
    zfill_w = len(str(num))
    h, w = size
    image_list = []
    for i in range(num):
        image = rand_color_image((h, w), sat=140, val=160)
        image = put_text_centered(image, f"{i}".zfill(zfill_w), cv2.FONT_HERSHEY_SIMPLEX, 30, (255, 255, 255), 60)
        image_list.append(image)
    return image_list


def gray_images(size: Tuple[int, int], num: int = 25) -> List[npt.NDArray[np.uint8]]:
    h, w = size
    image_list = []
    for i in range(num):
        image = np.full((h, w, 3), 128, dtype=np.uint8)
        image_list.append(image)
    return image_list
