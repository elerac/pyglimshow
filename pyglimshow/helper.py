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
    """Generate a random color image.

    Parameters
    ----------
    size : Tuple[int, int]
        Image size (width, height).
    hue : Optional[int], optional
        Hue value (0-179), by default None
    sat : Optional[int], optional
        Saturation value (0-255), by default None
    val : Optional[int], optional
        Value value (0-255), by default None

    Returns
    -------
    npt.NDArray[np.uint8]
        Random color image. (height, width, 3) shape.
    """

    w, h = size

    if hue is None:
        hue = np.random.randint(0, 180)
    if sat is None:
        sat = np.random.randint(0, 255)
    if val is None:
        val = np.random.randint(0, 255)

    color = cv2.cvtColor(np.array([[[hue, sat, val]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)
    img = np.full((h, w, 3), color, dtype=np.uint8)
    return img


def gen_countup_imglist(size: Tuple[int, int], num: int, hue: Optional[int] = None, sat: int = 140, val: int = 160) -> List[npt.NDArray[np.uint8]]:
    """Generate a list of images with count-up numbers.

    Parameters
    ----------
    size : Tuple[int, int]
        Image size (width, height).
    num : int
        Number of images.
    hue : Optional[int], optional
        Hue value (0-179), by default None
    sat : int, optional
        Saturation value (0-255), by default 140
    val : int, optional
        Value value (0-255), by default 160

    Returns
    -------
    List[npt.NDArray[np.uint8]]
        List of images. Each image has a count-up number.
    """

    zfill_w = len(str(num))
    w, h = size
    image_list = []
    for i in range(num):
        image = rand_color_image((h, w), hue, sat, val)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontscale = 30.0 * h / 2160.0
        color = (255, 255, 255)
        thickness = int(fontscale * 2)
        image = put_text_centered(image, f"{i}".zfill(zfill_w), font, fontscale, color, thickness)
        image_list.append(image)
    return image_list
