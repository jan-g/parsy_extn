import os.path
from setuptools import setup, find_packages


def read_file(fn):
    with open(os.path.join(os.path.dirname(__file__), fn)) as f:
        return f.read()

setup(
    name="parsy-extn",
    setup_requires=["setupmeta"],
    versioning="dev",
    url="http://github.com/jan-g/{name}",
    packages=find_packages(exclude=["test*"]),

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Text Processing",
    ],
)
