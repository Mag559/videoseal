from PIL import Image

from algorithm.bits_adapter import str_to_bits, bytes_to_bits, int_to_bits, bits_to_str, bits_to_bytes, bits_to_int
from algorithm.handle_model import Model
from algorithm.scramble import scramble

model: None | Model = None


def hide(message: str | bytes | int | list[int], key: int, img_path, out_path) -> None:
    """
    Hide the message in the image
    :param message: message to hide, converted to a list of bits from any of the currently supported types
    :param key: key used to determine the transform of the image in which the message is hidden
    :param img_path: cover image
    :param out_path: where to save the watermarked image

    First call takes longer due to the initialization of the neural network
    """
    global model
    if model is None:
        model = Model()

    img = Image.open(img_path).convert("RGB")
    if isinstance(message, str):
        msg = str_to_bits(message)
    elif isinstance(message, bytes):
        msg = bytes_to_bits(message)
    elif isinstance(message, int):
        msg = int_to_bits(message)
    else:
        msg = message

    img = scramble(img, key, False)
    img_w = model.hide_bits(img, msg)
    img_w = scramble(img_w, key, True)

    img_w.save(out_path)


def detect(message_type: type, key: int, img_path) -> str | bytes | int | list[int]:
    """
    Detect a message in the image
    :param message_type: what form to return the message in: string, bytes, int, otherwise list of bits
    :param key: key used to determine the transform of the image in which the message is hidden
    (the same as the one used to hide the message)
    :param img_path: watermarked image path
    :return: message of desired type
    """
    global model
    if model is None:
        model = Model()

    img_w = Image.open(img_path).convert("RGB")
    img_w = scramble(img_w, key, False)

    msg = model.detect_bits(img_w)
    if message_type.__name__ == "str":
        message = bits_to_str(msg)
    elif message_type.__name__ == "bytes":
        message = bits_to_bytes(msg)
    elif message_type.__name__ == "int":
        message = bits_to_int(msg)
    else:
        message = msg

    return message