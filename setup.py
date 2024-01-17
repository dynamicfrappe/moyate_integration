from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in moyate_integration/__init__.py
from moyate_integration import __version__ as version

setup(
	name="moyate_integration",
	version=version,
	description="moyate_integration",
	author="moyate_integration",
	author_email="dynmaic@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
