from hashlib import sha256
from math import log, ceil
from typing import Generator
from PIL import Image


P_BYTES = 70



def generate_pseudorandom_bytes(key: int) -> Generator[bytes, None, None]:
    """
    Generate pseudorandom bytes, based on a public key of up 70 `P_BYTES` bytes.
    Relies on the sha256 hash
    """
    counter: int = 0
    while True:
        data: bytes = key.to_bytes(P_BYTES) + counter.to_bytes(8, "big")
        yield sha256(data).digest()

        counter += 1


def generate_positions(total: int, key: int) -> Generator[int, None, None]:
    """
    Generates pseudorandom numbers between 0 (inclusive) and `total` (exclusive) in a non-repeating fashion
    Based on the `generate_pseudorandom_bytes` function
    """
    possible_positions: list[int] = [pos for pos in range(total)]

    gen = generate_pseudorandom_bytes(key)
    # do the Fisher-Yates shuffle
    rand_bytes: bytes = next(gen)
    required_bytes: int = ceil(log(len(possible_positions), 8))
    for i in range(len(possible_positions) - 1, 0, -1):

        if len(rand_bytes) < required_bytes:
            rand_bytes += next(gen)

        j = int.from_bytes(rand_bytes[:required_bytes], byteorder='big') % (i + 1)
        rand_bytes = rand_bytes[required_bytes:]
        possible_positions[i], possible_positions[j] = possible_positions[j], possible_positions[i]


    for pos in possible_positions:
        yield pos
    return



def scramble(image: Image.Image, key: int, reverse_mode: bool = False) -> Image.Image:
    """
    Creates a version of the image with the same size and pixels, but a radically different order of them
    Deterministic thanks to the use of the key and reversible using the reverse mode
    """
    image_with, image_height = image.size
    pixel_count = image_with * image_height


    old_pixels = list(image.getdata())

    new_pixels = [None] * pixel_count


    position_gen = generate_positions(pixel_count, key)

    if not reverse_mode:
        # for every position (i) in the NEW image
        # replace it with the i-th generated position in the OLD image
        for i in range(pixel_count):
            new_pixels[i] = old_pixels[next(position_gen)]
    else:
        # reverse mode (normal mode + reverse mode = original image)
        # for every position (i) in the OLD image
        # replace it with the i-th generated position in the NEW image
        for i in range(pixel_count):
            new_pixels[next(position_gen)] = old_pixels[i]


    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)

    return new_image



