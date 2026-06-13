from PIL import Image
from pathlib import Path

from handle_model import Model


def hide_and_save(model: Model, msg: list[int], img_path: Path, out_path: Path) -> None:
    # Load image.
    img = Image.open(img_path).convert("RGB")
    img_w = model.hide_bits(img, msg)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_w.save(out_path)


def detect_and_save(model: Model, img_w_path: Path, out_path: Path) -> None:
    img_w = Image.open(img_w_path).convert("RGB")
    result = model.detect_bits(img_w)
    with open(out_path, "w") as f:
        f.write(str(result))



if __name__ == "__main__":

    cover_images = Path("C:\\Users\\macie\\steg_images\\group0_premodified")
    decoded_path = Path("C:\\Users\\macie\\steg_images\\pseal\\found")
    encoded_path = Path("C:\\Users\\macie\\steg_images\\pseal\\modified")
    encoded_path2 = Path("C:\\Users\\macie\\steg_images\\pseal\\ready_to_read")
    stego_images = Path("C:\\Users\\macie\\steg_images\\pseal\\encoded")
    stego_images2 = Path("C:\\Users\\macie\\steg_images\\pseal\\encoded_detweaked")
    secondary_out_path = Path("C:\\Users\\macie\\steg_images\\pseal\\modified")

    model: Model = Model()

    msg = [1., 1., 1., 0., 0., 1., 1., 1., 0., 0., 1., 0., 0., 1., 1., 1., 0., 1.,
             1., 1., 0., 0., 1., 0., 0., 1., 1., 1., 0., 0., 0., 1., 1., 1., 1., 0.,
             0., 0., 0., 1., 1., 0., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 0., 1.,
             0., 0., 0., 1., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 1., 1., 1., 1.,
             0., 1., 0., 1., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 0., 0., 0., 1.,
             1., 1., 1., 0., 0., 0., 1., 0., 0., 1., 1., 0., 1., 0., 0., 0., 1., 1.,
             1., 1., 1., 0., 1., 1., 0., 0., 0., 1., 0., 1., 1., 1., 1., 1., 0., 0.,
             0., 0., 1., 1., 1., 1., 0., 0., 1., 1., 0., 0., 0., 0., 0., 1., 1., 0.,
             0., 1., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 0., 1., 1., 1.,
             0., 0., 0., 1., 0., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 0., 1., 1.,
             1., 0., 0., 0., 1., 0., 1., 1., 1., 0., 0., 1., 0., 0., 1., 0., 1., 1.,
             1., 1., 0., 1., 0., 1., 0., 1., 0., 1., 0., 0., 0., 1., 1., 0., 0., 1.,
             1., 1., 0., 0., 0., 1., 1., 0., 1., 1., 0., 0., 1., 1., 1., 1., 0., 0.,
             0., 0., 1., 0., 1., 1., 1., 1., 1., 1., 0., 0., 0., 0., 0., 1., 1., 1.,
             0., 0., 0., 0.]
    hide_and_save(model, msg,
                  Path(r"C:\Users\macie\GitHub\SteganographyProjects\videoseal\assets\imgs\1.jpg"), Path("test.png"))
    # recursive_process(
    #     cover_images,
    #     stego_images,
    #     lambda in_path, out_path: hide_and_save(model_, in_path, device_, out_path, msg_),
    # )

    # recursive_process(
    #     stego_images2,
    #     secondary_out_path,
    #     lambda in_path, out_path: hide_and_save(model_, in_path, device_, out_path.parent / "rehidden" / out_path.name, msg_),
    # )

    # recursive_process(
    #     encoded_path2,
    #     decoded_path,
    #     lambda in_path, out_path: detect_and_save(model_, in_path, device_, out_path.with_suffix(".txt"))
    # )