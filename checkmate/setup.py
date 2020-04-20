import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "checkmate-CrunchTime", 
    version = "0.0.1",
    author = "Crunch Time",
    author_email = "david.noble@eagles.oc.edu",
    description = "checkmate library",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/jme98/CrunchTimeCheckmate",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: None",
        "Operating System :: OS Independent"
    ],
    python_requires = '>=3.7.4'
)