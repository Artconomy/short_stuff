# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='short_stuff',
    version='1.0.1',
    author='Fox Danger Piacenti',
    author_email='fox@artconomy.com',
    description='Set of utilities for managing unique shortcodes.',
    download_url='https://github.com/Artconomy/short_stuff/archive/1.0.1.tar.gz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Artconomy/short_stuff",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ],
)
