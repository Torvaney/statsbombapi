from distutils.core import setup

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='statsbombapi',
    version='0.0.1-dev',
    packages=setuptools.find_packages(),
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
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
