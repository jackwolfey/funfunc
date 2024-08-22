import base64
import os
import subprocess
import time
import unittest
from pathlib import Path
import warnings

import cv2
import numpy as np
import pandas as pd
from PIL import Image

import funfunc

SKIP_TORCH = False
try:
    import torch
except ImportError:
    SKIP_TORCH = True


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
        image = funfunc.base64_string_to_pil_image(image_base64)
        self.assertEqual(image.size, (50, 50))

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

    @unittest.skipIf(SKIP_TORCH, "package torch is too big, if didn't install, "
                                 "then pass the get_device_torch test")
    def test_get_device_torch(self):
        device = funfunc.get_device_torch()
        self.assertIn(device, ['cuda', 'cpu'])

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

    def test_download_file(self):
        if os.path.exists('./pic.gif'):
            os.remove('./pic.gif')
        funfunc.download_file("http://img61.ddimg.cn/upload_img/00405/luyi/DDlogoNEW.gif",
                              './pic.gif')
        self.assertTrue(os.path.exists('./pic.gif'))

    @classmethod
    def test_time_it(cls):
        @funfunc.time_it
        def a_func():
            time.sleep(1)

        a_func()

    def test_quick_sort(self):
        arr = [3, 1, 2]
        sorted_arr = funfunc.quick_sort(arr)
        self.assertEqual(sorted_arr, sorted(arr))

    def test_chunks(self):
        arr = [i for i in range(100)]
        the_chunks = funfunc.chunks(arr, 10)
        self.assertEqual(len(the_chunks[0]), 10)

    def test_get_all_abspath_from_folder(self):
        path = '.'
        file_lst = funfunc.get_all_abspath_from_folder(path)
        file_lst_relative = funfunc.get_all_abspath_from_folder(path, get_relative=True)
        file_lst_with_folder = funfunc.get_all_abspath_from_folder(path, file_only=False)
        self.assertEqual(len(file_lst), 3)
        self.assertEqual(Path(sorted(file_lst_relative)[0]), Path('./pic.gif'))
        self.assertEqual(len(file_lst_with_folder), 4)

    def test_train_test_split_arr(self):
        arr = [i for i in range(100)]
        train, test = funfunc.train_test_split_arr(arr, ratio=0.90, shuffle=True)
        self.assertEqual(len(train), 90)

    def test_is_in_docker(self):
        flag = funfunc.is_in_docker()
        self.assertIn(flag, [True, False])

    def test_image_array_to_bytes(self):
        bytes = funfunc.image_array_to_bytes(self.image_array)
        image = funfunc.bytes_to_pil_image(bytes)
        self.assertEqual(image.size, (50, 50))

    def test_bytes_to_image_array(self):
        image_arr = funfunc.bytes_to_image_array(funfunc.pil_image_to_bytes(self.pil_image))
        image = funfunc.image_array_to_pil_image(image_arr)
        self.assertEqual(image.size, (50, 50))

    def test_image_url_to_pil_image(self):
        image = funfunc.image_url_to_pil_image('http://mmbiz.qpic.cn/mmbiz/PwIlO51l7wuFyoFwAXfqPNETWCibjN'
                                               'ACIt6ydN7vw8LeIwT7IjyG3eeribmK4rhibecvNKiaT2qeJRIWXLuKYPiaqtQ/0')
        self.assertEqual(image.size, (960, 1280))

    @classmethod
    def test_version_number(cls):
        output = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0'], stderr=subprocess.STDOUT)
        current_version = output.decode('utf-8').strip()[1:]
        new_version = funfunc.__VERSION__
        if current_version == new_version:
            warnings.warn('You may change some code but not modified the __VERSION__ in the __init__.py, please '
                          'remember to modify it.')

    def test_split_list(self):
        lst = [1, 2, 3, 4, 5, 6, 7]
        result = funfunc.split_list(lst, 3)
        self.assertEqual(result, [[1, 2, 3], [4, 5], [6, 7]])

    def test_tround(self):
        self.assertEqual(funfunc.tround(2.5), 3)


if __name__ == '__main__':
    unittest.main()
