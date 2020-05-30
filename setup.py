#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Master",
    author_email="roadmasternavi@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Typing :: Typed",
    ],
    description="Accesses to radiko API, gets media playlist URL and built header for HTTP request to its URL.",
    install_requires=["m3u8", "requests"],
    dependency_links=[],
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="radikoplaylist",
    name="radikoplaylist",
    packages=find_packages(include=["radikoplaylist", "radikoplaylist.*"]),
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=["pytest>=3"],
    url="https://github.com/road-master/radiko-playlist",
    version="1.0.1",
    zip_safe=False,
)
