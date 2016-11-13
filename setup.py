#!/usr/bin/env python

import sys, os
import setuptools


version = '1.0.2'


def long_description():
    """
    - pypi likes rst, Github prefers markdown
    - if README.rst exists use that
    - if README.md exists convert that to rst
    - pandoc README.md -o README.rst
    """
    return b''


def gather_requirements():
    """
    - define your requirements in requirements.txt
    - allow pinned requirements in requirements.txt but ignore the pin in setup.py
    - allow >= in requirements.txt and carry that through
    - ignore blank lines and comments in requirements.txt
    """
    requirements = []
    for r in open('requirements.txt').readlines():
        if not r.strip().startswith('#') and r.strip():
            if '==' in r:
                r = r.split('==')[0]
            requirements.append(r)
    return requirements


if sys.argv[-1] == 'publish':
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    sys.exit()


setuptools.setup(
    name='t',
    version=version,
    author='Brenton Cleeland',
    author_email='brenton@brntn.me',
    packages=setuptools.find_packages(),
    url='https://github.com/sesh/t',
    description='CLI for Toggl',
    entry_points={
        'console_scripts': [
            't = cli:cli',
        ]
    },
    install_requires=gather_requirements(),
    package_data={'': ['LICENSE', 'requirements.txt']},
    include_package_data=True,
    license='MIT License',
    classifiers=(
        b'Natural Language :: English',
        b'License :: OSI Approved :: MIT License',
        b'Programming Language :: Python :: 3',
        b'Programming Language :: Python :: 3.5',
    )
)
