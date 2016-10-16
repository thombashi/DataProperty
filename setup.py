import sys
import os.path
import setuptools


MISC_DIR = "misc"
REQUIREMENT_DIR = "requirements"

with open("README.rst") as fp:
    long_description = fp.read()

with open(os.path.join(MISC_DIR, "summary.txt")) as f:
    summary = f.read()

with open(os.path.join(REQUIREMENT_DIR, "requirements.txt")) as f:
    install_requires = [line.strip() for line in f if line.strip()]

with open(os.path.join(REQUIREMENT_DIR, "test_requirements.txt")) as f:
    tests_require = [line.strip() for line in f if line.strip()]

needs_pytest = set(["pytest", "test", "ptr"]).intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

author = "Tsuyoshi Hombashi"
email = "gogogo.vm@gmail.com"
project_name = "DataProperty"

setuptools.setup(
    name=project_name,
    version="0.10.0",
    url="https://github.com/thombashi/" + project_name,
    bugtrack_url="https://github.com/thombashi/{:s}/issues".format(
        project_name),

    author=author,
    author_email=email,
    description=summary,
    include_package_data=True,
    install_requires=install_requires,
    keywords=["data", "property"],
    license="MIT License",
    long_description=long_description,
    maintainer=author,
    maintainer_email=email,
    packages=setuptools.find_packages(exclude=["test*"]),
    setup_requires=[] + pytest_runner,
    tests_require=tests_require,

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
