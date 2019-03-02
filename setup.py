#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

# with open('README.rst') as readme_file:
#     readme = readme_file.read()
#
# with open('HISTORY.rst') as history_file:
#     history = history_file.read()

requirements = [

]

setup_requirements = [
    # TODO(exiva): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='Norse Joy',
    version='0.0.1',
    description="Discord bot for PGNC server",
    long_description="idk.",
    author="Travis La Marr",
    author_email='travis@lamarr.me',
    url='https://github.com/exiva/poGoRaidBot',
    packages=find_packages(include=['nursejoy']),
    entry_points={
        'console_scripts': [
            'poGoRaidBot=poGoRaidBot.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    dependency_links=['https://github.com/Rapptz/discord.py/tarball/rewrite#egg=discord.py-1.0'],
    license="MIT license",
    zip_safe=False,
    keywords='poGoRaidBot',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications :: Chat',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
