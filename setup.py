import setuptools

from distutils.core import setup


with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='statsbombapi',
    description='A wrapper for the Statsbomb API and public data.',
    version='0.0.1-dev',
    packages=setuptools.find_packages(),
    license='GPLv3+',
    long_description=readme,
    python_requires='>=3.7',
    install_requires=[
        'dataclasses-json>=0.4.2',
        'requests>=2.23.0'
    ],
    extras_require={
        'dev': [
            'pytest',
            'ipython',
            'mypy>=0.710',
            'hypothesis',
            'flake8',
            'simplejson'
        ]
    }
)
