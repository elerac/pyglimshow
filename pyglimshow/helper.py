from typing import Tuple, List, Optional
import numpy as np
import numpy.typing as npt
import cv2


def put_text_centered(img, text, font, fontscale, color, thickness):
    textsize = cv2.getTextSize(text, font, fontscale, thickness)[0]
    textX = (img.shape[1] - textsize[0]) / 2
    textY = (img.shape[0] + textsize[1]) / 2
    return cv2.putText(img, text, (int(textX), int(textY)), font, fontscale, color, thickness, cv2.LINE_AA)


def create_backround_image(shape: Tuple[int, int, int], hue: Optional[int] = None, sat: Optional[int] = None, val: Optional[int] = None) -> npt.NDArray[np.uint8]:
    """Create a random color image.

    Parameters
    ----------
    shape : Tuple[int, int, int]
        Shape of the image (height, width, 3).
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
    h, w, ch = shape
    if ch != 3:
        raise ValueError("The number of channels must be 3.")

    if hue is None:
        hue = np.random.randint(0, 180)
    if sat is None:
        sat = np.random.randint(0, 255)
    if val is None:
        val = np.random.randint(0, 255)

    color = cv2.cvtColor(np.array([[[hue, sat, val]]], dtype=np.uint8), cv2.COLOR_HSV2BGR)
    image = np.full((h, w, 3), color, dtype=np.uint8)
    return image


def create_number_image(shape: Tuple[int, int, int], i: int, hue: Optional[int] = None, sat: int = 140, val: int = 160) -> npt.NDArray[np.uint8]:
    """Create a image with the number at the center with the random color background.

    Parameters
    ----------
    shape : Tuple[int, int, int]
        Shape of the image (height, width, 3).
    i : int
        The number of images.
    hue : Optional[int], optional
        Hue value (0-179), by default None (random)
    sat : int, optional
        Saturation value (0-255), by default 140
    val : int, optional
        Value value (0-255), by default 160

    Returns
    -------
    npt.NDArray[np.uint8]
        Image with the number. (height, width, 3) shape.
    """

    zfill_w = max(3, len(str(i)))

    if i % 3 == 0:
        image = create_backround_image(shape, 0, sat, val)
    elif i % 3 == 1:
        image = create_backround_image(shape, 60, sat, val)
    else:
        image = create_backround_image(shape, 120, sat, val)

    h, w, _ = shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontscale = 30.0 * h / 2160.0
    color = (255, 255, 255)
    thickness = int(fontscale * 2)
    image = put_text_centered(image, f"{i}".zfill(zfill_w), font, fontscale, color, thickness)
    return image
