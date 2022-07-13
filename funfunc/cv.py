# -*- coding: utf-8 -*-
# AUTHOR  : wjia
# TIME    : 2022/6/21 16:32
# FILE    : cv
# PROJECT : funfunc
# IDE     : PyCharm
import base64
import io


def pil_image_to_base64_string(pil_image, image_format='.jpg') -> str:
    """
    conver PIL.Image object into base64string
    @param pil_image:PIL.Image object
    @param image_format:converted image format,default = '.jpg', it could also be '.png','.jpeg','.bmp'
    @return:base64string
    """
    temp_buffer = io.BytesIO()
    try:
        pil_image.save(temp_buffer, format=image_format)
    except Exception as e:
        raise NotImplementedError(f'pil_image has not method save(), is this a PIL.Image? {e}')
    byte_data = temp_buffer.getvalue()
    base64_string = base64.b64encode(byte_data).decode('utf-8')
    return base64_string


def base64_string_to_pil_image(image_base64_string: str):
    from PIL import Image

    img_b64decode = base64.b64decode(image_base64_string)
    image_bytes = io.BytesIO(img_b64decode)
    pil_image = Image.open(image_bytes)
    return pil_image


def pil_image_to_cv_image(pil_image):
    import cv2
    import numpy as np

    cv_image = cv2.cvtColor(np.asarray(pil_image), cv2.COLOR_RGB2BGR)
    return cv_image


def cv_image_to_pil_image(cv_image):
    import cv2
    from PIL import Image

    pil_image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))
    return pil_image


def cv_image_to_base64_string(cv_image, image_format='.jpg') -> str:
    """
    conver cv2 image object into base64string
    @param cv_image: cv2 image object
    @param image_format: converted image format,default = '.jpg', it could also be '.png','.jpeg','.bmp'
    @return: base64string
    """
    import cv2

    temp_string = cv2.imencode(image_format, cv_image)[1].tobytes()
    base64_string = base64.b64encode(temp_string).decode('utf-8')
    return base64_string


def base64_string_to_cv_image(base64_string: str):
    import cv2
    import numpy as np

    base64_decode = base64.b64decode(base64_string)
    cv_image = cv2.imdecode(np.frombuffer(base64_decode, np.uint8), cv2.COLOR_BGR2RGB)
    return cv_image


def rotate_image(img, degree: int):
    """
    rotate a cv image and return its rotation matrix
    @param img: cv image object
    @param degree: rotate degree, if its negative, do counterclockwise rotation
    """
    import cv2
    from math import fabs, sin, radians

    height, width = img.shape[:2]
    new_height = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    new_width = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    rotation_matrix = cv2.getRotationMatrix2D((width // 2, height // 2), degree, 1)

    rotation_matrix[0, 2] += (new_width - width) // 2
    rotation_matrix[1, 2] += (new_height - height) // 2

    rotated_img = cv2.warpAffine(img, rotation_matrix, (new_width, new_height), borderValue=(255, 255, 255))
    return rotated_img, rotation_matrix
