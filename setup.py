from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="mynodesdk",
    version="0.0.4",
    description="Tools for creating and managing myNode application package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mynodebtc/mynode_sdk",
    author="MYNODE",
    author_email="admin@mynodebtc.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="mynode, bitcoin, lightning, sdk, applications",
    packages=["mynodesdk"],
    python_requires=">=3.7, <4",
    entry_points={
        "console_scripts": [
            "mynode-sdk=mynodesdk.main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/mynodebtc/mynode_sdk/issues",
        "Source": "https://github.com/mynodebtc/mynode_sdk",
    },
)