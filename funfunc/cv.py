# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 16:32
# FILE    : cv
# PROJECT : funfunc
# IDE     : PyCharm
__all__ = [
    'pil_image_to_bytes',
    'pil_image_to_base64_string',
    'base64_string_to_pil_image',
    'pil_image_to_image_array',
    'image_array_to_pil_image',
    'image_array_to_bytes',
    'image_array_to_base64_string',
    'base64_string_to_image_array',
    'rotate_image',
    'bytes_to_pil_image',
    'bytes_to_image_array',
    'image_url_to_pil_image',
    'gen_ico_from_png'
]

import base64
import io
from pathlib import Path


def pil_image_to_bytes(pil_image) -> bytes:
    try:
        image_io = io.BytesIO()
        pil_image.save(image_io, format='PNG')
    except AttributeError as e:
        raise NotImplementedError(f'pil_image has not method save(), is this a PIL.Image.Image? {e}')
    return image_io.getvalue()


def pil_image_to_base64_string(pil_image) -> str:
    """
    conver PIL.Image object into base64string

    :param pil_image: PIL.Image object
    :return: base64string
    """
    return base64.b64encode(pil_image_to_bytes(pil_image)).decode('utf-8')


def base64_string_to_pil_image(image_base64_string: str):
    from PIL import Image

    img_b64decode = base64.b64decode(image_base64_string)
    image_bytes = io.BytesIO(img_b64decode)
    pil_image = Image.open(image_bytes)
    return pil_image


def pil_image_to_image_array(pil_image):
    import cv2
    import numpy as np

    image_array = cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_RGB2BGR)
    return image_array


def image_array_to_pil_image(image_array):
    import cv2
    from PIL import Image

    pil_image = Image.fromarray(cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB))
    return pil_image


def image_array_to_bytes(image_array, image_format='.png'):
    import cv2

    imencode = cv2.imencode(image_format, image_array)
    if imencode[0]:
        encoded_image = imencode[1]
        return encoded_image.tobytes()
    else:
        raise ValueError(f'This image_array couldn\'t encode to \'{image_format}\' format, '
                         f'please try something else.')


def image_array_to_base64_string(image_array, image_format='.png') -> str:
    """
    conver numpy array image object into base64string

    :param image_array: numpy array image object
    :param image_format: converted image format,default = '.png', it could also be '.jpg','.jpeg','.bmp'
    :return: base64string
    """
    temp_string = image_array_to_bytes(image_array, image_format)
    base64_string = base64.b64encode(temp_string).decode('utf-8')
    return base64_string


def base64_string_to_image_array(base64_string: str):
    import cv2
    import numpy as np

    base64_decode = base64.b64decode(base64_string)
    image_array = cv2.imdecode(np.frombuffer(base64_decode, np.uint8), cv2.COLOR_BGR2RGB)
    return image_array


def rotate_image(image_array, degree: int):
    """
    rotate a cv image and return its rotation matrix

    :param image_array: image array object
    :param degree: rotate degree, if it's negative, do counterclockwise rotation
    """
    import cv2
    from math import fabs, sin, radians, cos

    height, width = image_array.shape[:2]
    new_height = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    new_width = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)

    rotation_matrix[0, 2] += (new_width - width) // 2
    rotation_matrix[1, 2] += (new_height - height) // 2

    rotated_img = cv2.warpAffine(image_array, rotation_matrix, (new_width, new_height), borderValue=(255, 255, 255))
    return rotated_img, rotation_matrix


def bytes_to_pil_image(image_bytes: bytes):
    from io import BytesIO
    from PIL import Image

    return Image.open(BytesIO(image_bytes))


def bytes_to_image_array(image_bytes: bytes):
    import numpy as np
    import cv2

    image_array = np.array(bytes_to_pil_image(image_bytes))
    return cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)


def image_url_to_pil_image(image_url: str, check_headers: bool = False):
    from io import BytesIO
    import requests
    from PIL import Image

    request = requests.get(image_url)
    if check_headers:
        content_type = request.headers.get('Content-Type', '')
        assert content_type.split(r'/')[0] == 'image', \
            "The request file's Content-Type is not image, please check the URL."

    return Image.open(BytesIO(request.content))


def gen_ico_from_png(png_file_path: str, output_path: str = None):
    from PIL import Image

    png_path = Path(png_file_path)
    img = Image.open(png_path)
    if output_path is None:
        img.save(png_path.parent.joinpath(png_path.stem + '.ico'), format='ICO', sizes=[img.size])
    else:
        img.save(output_path, format='ICO', sizes=[img.size])
