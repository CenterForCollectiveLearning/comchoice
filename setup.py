import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pairchoice",
    version="0.0.1",
    author="cnavarreteliz",
    author_email="cnavarreteliz@gmail.com",
    description="Toolkit to analyze pairwise comparison data",
    long_description=long_description,
    url="https://github.com/CenterForCollectiveLearning/pairchoice",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
)