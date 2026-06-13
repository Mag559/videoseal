from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

from scramble import scramble



def shift_channels(img: Image.Image, offset) -> Image.Image:
    r, g, b = img.split()
    shift = lambda i: (i + offset) % 256
    r = r.point(shift)
    g = g.point(shift)
    b = b.point(shift)

    return Image.merge("RGB", (r, g, b))


def swap_channels(img: Image.Image, forward: bool) -> Image.Image:
    r, g, b = img.split()
    if forward:
        return Image.merge("RGB", (b, r, g))
    else:
        return Image.merge("RGB", (g, b, r))


def transform(image_path: Path, out_dir: Path, changes: dict[str, Callable]):
    image = Image.open(image_path)

    for parent in image_path.parents[:3]:
        if parent.name in changes.keys():
            # there are already directories matching the change structure
            # only perform the transform relevant for this directory
            out_dir.mkdir(parents=True, exist_ok=True)
            changes[parent.name](image).save(out_dir / image_path.with_suffix(".png").name)
            break
    else:
        # no directory structure matching the changes yet
        for change in changes.keys():
            (out_dir / f"{change}").mkdir(parents=True, exist_ok=True)
            changes[change](image).save(out_dir / f"{change}" / image_path.with_suffix(".png").name)
        return


transforms = {
        'offset': lambda image: ImageChops.offset(image, image.size[0] // 2, image.size[1] // 2),
        'mirror': lambda image: ImageOps.flip(ImageOps.mirror(image)),
        'shifted_channels': lambda image: shift_channels(image, 30),
        'swapped_channels': lambda image: swap_channels(image, True),
        'permuted': lambda image: scramble(image, 123456, False),
        'reference_transform': lambda image: image,
    }


reverse_transforms = {
    'offset': lambda image: ImageChops.offset(image, -1 * (image.size[0] // 2), -1 * (image.size[1] // 2)),
    'mirror': lambda image: ImageOps.flip(ImageOps.mirror(image)),
    'shifted_channels': lambda image: shift_channels(image, -30),
    'swapped_channels': lambda image: swap_channels(image, False),
    'permuted': lambda image: scramble(image, 123456, True),
    'reference_transform': lambda image: image,
}

