# setup.py

from setuptools import setup, find_packages

setup(
    name='stock_prediction_app',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'sqlalchemy',
        'pymysql',
        'tensorflow',
        'keras',
        'flask'
    ],
)