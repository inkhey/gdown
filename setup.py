from __future__ import print_function

import distutils.spawn
import re
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "gdown/__init__.py"
    with open(filename) as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


version = get_version()


if sys.argv[1] == "release":
    if not distutils.spawn.find_executable("twine"):
        print(
            "Please install twine:\n\n\tpip install twine\n", file=sys.stderr
        )
        sys.exit(1)

    try:
        import github2pypi  # NOQA
    except ImportError:
        print(
            "Please install github2pypi:\n\n\tpip install github2pypi\n",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        import build  # NOQA
    except ImportError:
        print(
            "Please install build:\n\n\tpip install build\n", file=sys.stderr
        )
        sys.exit(1)

    commands = [
        "git pull origin main",
        "git tag v{:s}".format(version),
        "git push origin main --tags",
        "python -m build",
        "twine upload dist/gdown-{:s}*".format(version),
    ]
    for cmd in commands:
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()

    try:
        import github2pypi

        return github2pypi.replace_url(
            slug="wkentaro/gdown", content=long_description
        )
    except Exception:
        return long_description


setup(
    name="gdown",
    version=version,
    packages=find_packages(exclude=["github2pypi"]),
    install_requires=[
        "filelock",
        "requests[socks]",
        "six",
        "tqdm",
        "beautifulsoup4",
    ],
    description="Google Drive direct download of big files.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Kentaro Wada",
    author_email="www.kentaro.wada@gmail.com",
    url="http://github.com/wkentaro/gdown",
    license="MIT",
    keywords="Data Download",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["gdown=gdown.cli:main"]},
)
