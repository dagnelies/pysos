from setuptools import setup
import pathlib


setup(
    name='pysos',
    version='1.3.0',
    py_modules=['pysos'],
    scripts=['pysos.py'],
    description='Simple Object Storage - Persistent dicts and lists for python.',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/dagnelies/pysos',
    author='Arnaud Dagnelies',
    author_email='arnaud.dagnelies@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
    ],
    keywords='persistent persistence dict list file',
    install_requires=['chardet']
)
