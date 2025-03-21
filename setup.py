from setuptools import find_packages, setup

setup(
    name="phrame-mental-maps",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "pandas",
        "numpy"
    ],
)
