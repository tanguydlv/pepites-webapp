import os
from setuptools import setup, find_packages

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    requirements = f.readlines()

setup(
    name='pepites-webapp',
    version='0.0.1',
    description='Fullstack application to manage user accounts for Pepites',
    url='',
    author='tanguydlv',
    author_email='tvillegeorges@gmail.com',
    license='proprietary',
    packages=find_packages(),
    install_requires=requirements
)
