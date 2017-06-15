# -*- coding: utf-8 -*-
from setuptools import setup
import sys

PY_VERSION = sys.version_info[0], sys.version_info[1]

if PY_VERSION < (3, 0):
    long_description = open('README.md').read()
else:
    long_description = open('README.md', encoding='utf-8').read()

setup(
    name='drf-nested-decorator',
    version='0.5',
    author=u'Zowie Langdon',
    author_email='zowie@akoten.com',
    packages=['drf_nested_decorator'],
    url='https://github.com/luminum-solutions/drf-nested-decorator',
    license='MIT',
    description='An extra decorator for Django Rest Framework that allows methods of a viewset to accept a nested key.',
    long_description=long_description,
    zip_safe=False,
    install_requires=['djangorestframework>=3.1.3'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
    ],
)
