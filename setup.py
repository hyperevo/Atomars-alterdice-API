#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

deps = {
    'api': [
        "aiohttp==3.5.4",
        "eth_utils==1.8.1",
    ]
}

install_requires =  deps['api']

setup(
    name='Atomars and Alterdice Python API',
    version='0.1.1',
    description='An unofficial python library for communication with the Atomars and Alterdice exchanges API',
    author='Tommy Mckinnon',
    author_email='tommy@HeliosProtocol.io',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=deps,
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=['setuptools-markdown'],
    license='MIT',
    zip_safe=False,
)
