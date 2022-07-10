from setuptools import setup

setup(
    name="clipper",
    version="0.0.1",
    entry_points={"console_scripts": ["clipper = clipper:main"]},
    install_requires=["tinydb", "reportlab"],
)
