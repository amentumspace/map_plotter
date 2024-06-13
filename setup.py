import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="map_plotter",
    version="0.3.0",
    author="Amentum Scientific",
    author_email="team@amentum.space",
    description="A simple Python package to plot a gridded quantity overlaid onto geographic map",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amentumspace/map_plotter",
    packages=setuptools.find_packages(),
    install_requires=requirements,
)