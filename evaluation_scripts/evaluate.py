from PIL import Image
import cv2
import numpy
from pathlib import Path

from evaluation_scripts.directory_processor import recursive_process
from evaluation_scripts.attacks import attack_and_save, specified_attacks
from evaluation_scripts.text_diff import diff_main
from evaluation_scripts.transforms import transform, transforms, reverse_transforms
from algorithm.handle_model import Model


def hide_and_save(model: Model, msg: list[int], img_path: Path, out_path: Path) -> None:
    # Load image.
    img = Image.open(img_path).convert("RGB")
    img_w = model.hide_bits(img, msg)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_w.save(out_path)


def detect_and_save(model: Model, img_w_path: Path, out_path: Path) -> None:
    img_w = Image.open(img_w_path).convert("RGB")
    result = model.detect_bits(img_w)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(str(result))


def rehide(model, opencv_image):
    # source: https://stackoverflow.com/questions/43232813/convert-opencv-image-format-to-pil-image-format

    # convert from openCV2 to PIL. Notice the COLOR_BGR2RGB which means that
    # the color is converted from BGR to RGB
    color_converted = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(color_converted)

    pil_image = model.hide_bits(pil_image, replacement_msg)

    # use numpy to convert the pil_image into a numpy array
    numpy_image = numpy.array(pil_image)

    # convert to a openCV2 image, notice the COLOR_RGB2BGR which means that
    # the colour is converted from RGB to BGR format
    return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    master_path = Path("C:\\Users\\macie\\steg_images")
    cover_images = master_path / "group1"
    transformed_covers = master_path / "group1_pretransformed"

    model_path: Path = master_path / "vseal1"

    transformed_watermarked = model_path / "watermarked_t"
    watermarked = model_path / "watermarked"

    attacked = model_path / "attacked"

    transformed_attacked = model_path / "transformed_attacked"
    found = model_path / "found"

    vseal: Model = Model()

    msg = [1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1,
             1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0,
             0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1,
             0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1,
             0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1,
             1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1,
             1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0,
             0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0,
             0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1,
             0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1,
             1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1,
             1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1,
             1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0,
             0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1,
             0, 0, 0, 0]

    replacement_msg = [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1,
        1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0,
        0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0,
        1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
        0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1,
        0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1,
        0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1,
        1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1,
        1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1,
        1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0,
        1, 1, 1, 1]

    # transform before watermarking
    recursive_process(
        cover_images,
        transformed_covers,
        lambda in_image, out_image: transform(in_image, out_image.parent, transforms)
    )

    # watermark
    recursive_process(
        transformed_covers,
        transformed_watermarked,
        lambda in_image, out_image: hide_and_save(vseal, msg, in_image, out_image)
    )

    # reverse transform to get image looking like the original
    recursive_process(
        transformed_watermarked,
        watermarked,
        lambda in_image, out_image: transform(in_image, out_image.parent, reverse_transforms)
    )

    # attack the image to test robustness

    # embed a secondary watermark in the untransformed version of the image
    specified_attacks["rehide"] = lambda image: rehide(vseal, image)

    recursive_process(
        watermarked,
        attacked,
        lambda in_image, out_image: attack_and_save(in_image, out_image.parent, specified_attacks)
    )

    # transform images before detecting the watermark
    recursive_process(
        attacked,
        transformed_attacked,
        lambda in_image, out_image: transform(in_image, out_image.parent, transforms)
    )


    # detect the watermark
    recursive_process(
        transformed_attacked,
        found,
        lambda in_image, out_file: detect_and_save(vseal, in_image, out_file.with_suffix(".txt"))
    )

    diff_main(found, str(msg), str(replacement_msg))
    print("Note: replacement message and original message were embedded in different transforms of the image."
          " Detection takes place in the transform used for embedding the original message."
          " Not being able to read the replacement and being able to read the original is the expected result."
          " Replacement would be possible to read in the transform it was embedded in.")