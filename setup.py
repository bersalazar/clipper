from setuptools import setup

setup(
    name = 'clipper',
    version = '0.0.1',
    packages = ['cli'],
    entry_points = {
        'console_scripts': [
            'clipper = cli.__main__:main'
        ]
    }
)
