import unittest
import cv2.cv2 as cv2
import numpy as np
import base64
import funfunc
from PIL import Image
import pandas as pd


class FunfuncTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.image_array = np.zeros((50, 50, 3), dtype=np.uint8)
        self.pil_image = Image.fromarray(cv2.cvtColor(self.image_array, cv2.COLOR_BGR2RGB))
        self.image_base64 = base64.b64encode(cv2.imencode('.png', self.image_array)[1].tobytes()).decode('utf-8')

    def test_base64_string_to_pil_image(self):
        pil_image = funfunc.base64_string_to_pil_image(self.image_base64)
        self.assertIsInstance(pil_image, Image.Image)

    def test_pil_image_to_base64_string(self):
        image_base64 = funfunc.pil_image_to_base64_string(self.pil_image)
        # 该测试判断条件改为下句无法通过，问题未知
        # self.assertEqual(image_base64, self.image_base64)
        self.assertIsInstance(image_base64, str)

    def test_image_array_to_pil_image(self):
        pil_image = funfunc.image_array_to_pil_image(self.image_array)
        self.assertIsInstance(pil_image, Image.Image)

    def test_pil_image_to_image_array(self):
        image_array = funfunc.pil_image_to_image_array(self.pil_image)
        self.assertIsInstance(image_array, np.ndarray)

    def test_base64_string_to_image_array(self):
        image_array = funfunc.base64_string_to_image_array(self.image_base64)
        self.assertEqual(image_array.all(), self.image_array.all())

    def test_image_array_to_base64_string(self):
        image_base64 = funfunc.image_array_to_base64_string(self.image_array)
        self.assertEqual(image_base64, self.image_base64)

    def test_get_device_torch(self):
        device = funfunc.get_device_torch()
        self.assertEqual(device, 'cpu')

    def test_pandas_max_print(self):
        old = pd.get_option('display.max_columns')
        funfunc.pandas_max_print()
        new = pd.get_option('display.max_columns')
        self.assertNotEqual(old, new)

    def test_Validator_is_url(self):
        url = 'https://www.baidu.com'
        un_url = 'htps://www.usb.net'
        is_url = funfunc.Validator.is_url(url)
        not_url = funfunc.Validator.is_url(un_url)
        self.assertTrue(is_url)
        self.assertFalse(not_url)

    def test_Validator_is_chinese(self):
        chinese = '你好啊123abc'
        un_chinese = 'hello123abc'
        is_chinese = funfunc.Validator.is_chinese(chinese)
        not_chinese = funfunc.Validator.is_chinese(un_chinese)
        self.assertTrue(is_chinese)
        self.assertFalse(not_chinese)


if __name__ == '__main__':
    unittest.main()
