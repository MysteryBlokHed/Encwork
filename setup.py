import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="encwork",
    version="1.0.3",
    author="Adam Thompson-Sharpe",
    author_email="adamthompsonsharpe@gmail.com",
    description="RSA-encrypted communication software written in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MysteryBlokHed/Encwork",
    packages=setuptools.find_packages(),
    install_requires=[
        "cryptography>=2.8"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
