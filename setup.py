#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versioneer

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='bibletk',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Toolkit for bible",
    long_description=readme,
    author="Chia-Jung, Yang",
    author_email='jeroyang@gmail.com',
    url='https://github.com/jeroyang/bibletk',
    packages=['bibletk'],
    package_data={
                'bibletk': ['bibletk/*.txt'],
                },
    include_package_data=True,
    data_files='',
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='bibletk',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Traditional Chinese',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

