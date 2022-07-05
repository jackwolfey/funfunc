# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import funfunc

setup(name="funfunc",
      version=funfunc.__VERSION__,
      description="Make Python Development Much Easier & Fun",
      long_description="Make Python Development Much Easier & Fun",
      author="Wei Jia",
      author_email="437160499@163.com",
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3']
      )

# python setup.py sdist bdist_wheel
# python -m twine upload --repository pypi dist/*
