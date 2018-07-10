#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from __future__ import absolute_import, print_function

import io
import os
import re
from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


setup(
    name='{{cookiecutter.project_slug}}',
    version='{{cookiecutter.version}}',
    description="{{cookiecutter.project_description}}",
    long_description='%s' % (
        re.compile(
            '^' + re.escape('[//]: # (start-badges)') + '.*^'
            + re.escape('[//]: # (end-badges)'), re.M | re.S
        ).sub('', read('README.md')),
    ),
    # In the future this will correctly render Markdown on PyPi:
    # long_description_content_type='text/markdown',
    author='{{cookiecutter.author_name}}',
    author_email='{{cookiecutter.author_email}}',
    url='https://{{cookiecutter.project_domain}}',
    packages=find_packages('src'),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    zip_safe=False,
    # keywords=[
    #     "keyword1", "keyword2", "..."
    # ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        '{{cookiecutter.license}}',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Printing',
    ],
    # List run-time dependencies HERE.  These will be installed by pip when
    # your project is installed. For an analysis of 'install_requires' vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        # Since we are describing application and not pip package, we use
        # requirements.txt to totally lock versions. This wouldn't be a good
        # idea when building a package.
        ln for ln in [
            re.compile('#.*').sub('', ln).strip()
            for ln in read('requirements.txt').split('\n')
        ] if ln
    ],
    # List additional groups of dependencies HERE (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev]
    extras_require={
        'dev': [
            'pycodestyle',
            'yapf',
            'bumpversion',
            'isort',
            'check-manifest',
            'pylint',

            # Docs and viewers
            'sphinx',
            'sphinx_rtd_theme',
            'm2r',

            # py.test stuff
            'pytest >= 3.0.0',
            'pytest-sugar',
            'pytest-spec',
            'pytest-mock',
            'factory-boy',
            'faker'
        ]
    },
    entry_points={
        'console_scripts': [
            '{{cookiecutter.project_slug}} = {{cookiecutter.project_slug}}.scripts:cli',
        ]
    },
    # scripts=[
    #     'bin/example_installable_script.sh'
    # ]
)
