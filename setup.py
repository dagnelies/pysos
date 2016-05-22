from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pysos',

    version='1.0.1',

    description='Simple Object Storage - Persistent dicts and lists for python.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/dagnelies/pysos',

    # Author details
    author='Arnaud Dagnelies',
    author_email='arnaud.dagnelies@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='persistent persistence dict list file',
    py_modules=["pysos"]
)