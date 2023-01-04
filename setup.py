import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comchoice",
    version="0.1.2",
    author="cnavarreteliz",
    author_email="cnavarreteliz@gmail.com",
    description="ComChoice (Computational Choice) is a large collection of many well-known voting rules and aggregation methods in Python.",
    license_files=("LICENSE.md",),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CenterForCollectiveLearning/comchoice",
    packages=setuptools.find_packages(),
    install_requires=[
        "fastapi",
        "networkx",
        "numpy",
        "pandas",
        "requests",
        "scipy",
        "tqdm"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
)
