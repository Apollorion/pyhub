from setuptools import setup, find_packages
from pyhub.__version__ import __version__

setup(
    name='pyhub',
    version=__version__,
    py_modules=['pyhub'],
    python_requires='~=3.10',
    packages=find_packages(),
    install_requires=[
        'pyyaml==6.0',
    ]
)