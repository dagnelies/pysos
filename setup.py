from setuptools import setup, find_packages


setup(
    name='pysos',
    version='1.2.6',
    py_modules=['pysos'],
    scripts=['pysos.py'],
    description='Simple Object Storage - Persistent dicts and lists for python.',
    url='https://github.com/dagnelies/pysos',
    author='Arnaud Dagnelies',
    author_email='arnaud.dagnelies@gmail.com',
    license='MIT',
    classifiers=[],
    keywords='persistent persistence dict list file',
    install_requires=['chardet']
)
