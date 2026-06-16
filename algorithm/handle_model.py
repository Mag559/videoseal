import torch
from PIL import Image
from torchvision.transforms.functional import to_tensor, to_pil_image


class Model:
    """
    Api for the inner pytorch workings
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # load the jit model
        self.model = torch.jit.load("ckpts/y_256b_img.jit")
        self.model.to(self.device)
        self.model.eval()


    def bits_to_tensor(self, bits: list[int]) -> torch.Tensor:
        return torch.tensor([bits]).float().to(self.device)


    @staticmethod
    def tensor_to_bits(tensor: torch.Tensor) -> list[int]:
        return tensor.int().tolist()[0]


    def hide_bits(self, img: Image.Image, bits: list[int]) -> Image.Image:
        return self.hide_tensor(img, self.bits_to_tensor(bits))


    def detect_bits(self, img: Image.Image) -> list[int]:
        return Model.tensor_to_bits(self.detect_tensor(img))


    def hide_tensor(self, img: Image.Image, msg: torch.Tensor) -> Image.Image:
        img_o = to_tensor(img).unsqueeze(0).float().to(self.device)

        # Option 2: Embedding only.
        with torch.no_grad():
            # Returns watermarked image directly.
            img_w = self.model.embed(img_o, msg, is_video=False)

        # Convert back to PIL Image for saving.
        return to_pil_image(img_w.squeeze().cpu())


    def detect_tensor(self, img: Image.Image) -> torch.Tensor:
        # Option 3: Detection only.
        img = to_tensor(img).unsqueeze(0).float().to(self.device)
        with torch.no_grad():
            # Returns predictions tensor directly.
            predictions = self.model.detect(img, is_video=False)

            # Process predictions to get binary message.
            # Assuming first channel is detection mask and rest are bit predictions.
            bit_predictions = predictions[:, 1:]  # Exclude mask
            detected_message = (bit_predictions > 0).float()  # Threshold
        return detected_message



