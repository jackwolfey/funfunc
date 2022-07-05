# funfunc
**Implement multiple functions or tool classes to make your Python Development Much Easier & Fun**

## Installation
```
pip install funfunc
```

## Usage
### Convert your opencv image object to base64 format string
```
import funfunc
import cv2

cv_image = cv2.imread('/img/path.jpg')
base64_string = funfunc.cv_image_to_base64_string(cv_image)
```
### Print a function runing time
```
import funfunc

@funfunc.time_it
def simple_func():
    for i in range(100000):
        print(i)
```
### Split a list to train and test set by a specific ratio
```
import funfunc

lst = [1, 2, 3, 4, 5, 6, 7, 8]
train_set, test_set = funfunc.train_test_split_arr(arr=lst, ratio=0.2)
```
### Check whether the string is a URL
```
from funfunc import Validator

Validator.is_url('http://www.github.com')
```

### And more functions wait you to explorer...