from collections.abc import Callable

import torch
from PIL import Image
from torchvision.transforms.functional import to_tensor, to_pil_image
from pathlib import Path


def recursive_process(input_directory: Path, output_directory, task: Callable[[Path, Path], None]) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    for item in input_directory.iterdir():
        # if item.name == "rehidden":
        #     continue
        if item.is_dir():
            (output_directory / item.name).mkdir(parents=True, exist_ok=True)
            recursive_process(item, output_directory / item.name, task)
            continue

        print(f"Processing {item}")
        task(item, output_directory / item.name)


def hide(model, img, device, msg):
    img_o = to_tensor(img).unsqueeze(0).float().to(device)

    # Option 2: Embedding only.
    with torch.no_grad():
        # Returns watermarked image directly.
        img_w = model.embed(img_o, msg, is_video=False)

    # Convert back to PIL Image for saving.
    return to_pil_image(img_w.squeeze().cpu())


def hide_and_save(model, img_path, device, out_path, msg):
    # Load image.
    img = Image.open(img_path).convert("RGB")
    img_w = hide(model, img, device, msg)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_w.save(out_path)


def detect(model, img_w, device):
    # Option 3: Detection only.

    img_w = to_tensor(img_w).unsqueeze(0).float().to(device)
    with torch.no_grad():
        # Returns predictions tensor directly.
        preds = model.detect(img_w, is_video=False)

        # Process predictions to get binary message.
        # Assuming first channel is detection mask and rest are bit predictions.
        bit_preds = preds[:, 1:]  # Exclude mask
        detected_message = (bit_preds > 0).float()  # Threshold
    return detected_message


def detect_and_save(model, img_w_path, device, out_path):
    img_w = Image.open(img_w_path).convert("RGB")
    result = detect(model, img_w, device)
    with open(out_path, "w") as f:
        f.write(str(result))


def load():
    # Load the JIT model.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = torch.jit.load("ckpts/y_256b_img.jit")
    model.to(device)
    model.eval()

    # Create a message to embed (random binary vector of 256bits).
    msg = torch.tensor([[1., 1., 1., 0., 0., 1., 1., 1., 0., 0., 1., 0., 0., 1., 1., 1., 0., 1.,
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
                         0., 0., 0., 0.]]).to(device)

    msg2 = torch.tensor([[0., 1., 1., 1., 1., 1., 0., 1., 0., 0., 0., 0., 1., 1., 0., 0., 0., 1.,
         1., 0., 1., 1., 0., 0., 1., 1., 0., 0., 0., 0., 0., 1., 1., 0., 1., 0.,
         0., 0., 1., 1., 0., 0., 1., 1., 1., 0., 1., 1., 1., 0., 1., 0., 0., 0.,
         0., 1., 0., 0., 0., 0., 0., 1., 0., 0., 0., 1., 1., 1., 1., 1., 1., 0.,
         0., 0., 0., 1., 0., 0., 1., 1., 1., 0., 1., 0., 1., 0., 0., 1., 1., 0.,
         1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 1., 1., 0., 1., 1., 1., 1., 1.,
         0., 1., 1., 1., 0., 1., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 1., 0.,
         0., 0., 0., 1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 0., 0., 0., 1.,
         0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 1., 1., 1., 0., 0., 1., 0., 1.,
         0., 1., 1., 1., 0., 0., 1., 1., 1., 1., 1., 0., 0., 0., 0., 1., 1., 0.,
         0., 0., 0., 1., 1., 1., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 1., 1.,
         1., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 1.,
         1., 1., 0., 1., 0., 1., 0., 1., 1., 0., 0., 0., 0., 1., 1., 0., 1., 1.,
         1., 1., 1., 0., 0., 0., 0., 1., 1., 0., 0., 0., 0., 0., 1., 1., 1., 0.,
         1., 1., 1., 1.]]).to(device)
    return model, device, msg2



if __name__ == "__main__":
    model_, device_, msg_ = load()

    cover_images = Path("C:\\Users\\macie\\steg_images\\group0_premodified")
    decoded_path = Path("C:\\Users\\macie\\steg_images\\pseal\\found")
    encoded_path = Path("C:\\Users\\macie\\steg_images\\pseal\\modified")
    encoded_path2 = Path("C:\\Users\\macie\\steg_images\\pseal\\ready_to_read")
    stego_images = Path("C:\\Users\\macie\\steg_images\\pseal\\encoded")
    stego_images2 = Path("C:\\Users\\macie\\steg_images\\pseal\\encoded_detweaked")
    secondary_out_path = Path("C:\\Users\\macie\\steg_images\\pseal\\modified")

    hide_and_save(model_, Path(r"C:\Users\macie\GitHub\SteganographyProjects\videoseal\assets\imgs\1.jpg"), device_, Path("test.png"), msg_)
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