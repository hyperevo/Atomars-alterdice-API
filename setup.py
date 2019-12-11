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

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='atom_alter_api',
    version='0.1.4',
    description='An unofficial python library for communication with the Atomars and Alterdice exchanges API',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/hyperevo/Atomars-alterdice-API",
    author='Tommy Mckinnon',
    author_email='tommy@HeliosProtocol.io',
    include_package_data=True,
    install_requires=install_requires,
    extras_require=deps,
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=['setuptools-markdown'],
    license='MIT',
    zip_safe=False,
    python_requires='>=3.6',
)
