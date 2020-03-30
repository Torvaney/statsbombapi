from distutils.core import setup

ith open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='statsbombapi',
    version='0.0.1-dev',
    packages=['statsbombapi',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=readme,
    python_requires='>=3.6',
    install_requires=[
        'dataclasses;python_version=="3.6"',
        'marshmallow>=3.3.0,<4.0.0',
        'marshmallow-enum>=1.5.1,<2.0.0',
        'typing-inspect>=0.4.0',
        'stringcase==1.2.0,<2.0.0'
    ],
    extras_require={
        'dev': [
            'pytest',
            'ipython',
            'mypy>=0.710',
            'hypothesis',
            'portray',
            'flake8',
            'simplejson'
        ]
    }
)
