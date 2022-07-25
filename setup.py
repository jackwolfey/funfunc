# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
import funfunc

setup(name="funfunc",
      version=funfunc.__VERSION__,
      description=funfunc.__DESCRIPTION__,
      long_description=funfunc.__DESCRIPTION__,
      url="https://github.com/jackwolfey/funfunc",
      author="Wei Jia",
      author_email="437160499@163.com",
      packages=find_packages(exclude='test'),
      platforms=["all"],
      classifiers=[
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12'],
      python_requires='>=3.8'
      )
