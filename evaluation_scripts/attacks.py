from collections.abc import Callable
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter
import cv2


def blur(img, sigma):
    attacked = gaussian_filter(img, sigma)
    return attacked


def awgn(img, std):
    mean = 0.0
    attacked = img + np.random.normal(mean, std, img.shape)
    attacked = np.clip(attacked, 0, 255)
    return attacked.astype(np.uint8)


def change_brightness(img, brightness):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.add(hsv[:, :, 2], brightness)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def zero_lsb(img, bits=1):
    mask = 0xFF << bits & 0xFF
    return img & mask


def reduce_color_depth(img, levels=32):
    step = 256 // levels
    reduced = (img // step) * step
    return reduced.astype(np.uint8)


def attack_and_save(image_path: Path, out_dir: Path, attacks: dict[str, Callable]):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    for attack in attacks.keys():
        (out_dir / f"{attack}").mkdir(parents=True, exist_ok=True)
        cv2.imwrite(out_dir / f"{attack}" / image_path.name, attacks[attack](image))
#             [int(cv2.IMWRITE_JPEG_QUALITY), 100]


specified_attacks = {
    'blur': lambda image: blur(image, [1, 1, 0]),
    'awgn': lambda image: awgn(image, 3),
    'brightness': lambda image: change_brightness(image, 3),
    'zero_lsb': lambda image: zero_lsb(image, 2),
    'reduce_color_depth': lambda image: reduce_color_depth(image, 80),
    'reference_attack': lambda image: image,
}