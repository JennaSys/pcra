from setuptools import setup, find_packages
import pathlib
import sys


# The directory containing this file
project_folder = pathlib.Path(__file__).parent


sys.path.append(str(project_folder))
from pcra import __version__


def glob_fix(package_name, glob):
    # this assumes setup.py lives in the folder that contains the package
    package_path = pathlib.Path(f'./{package_name}').resolve()
    return [str(path.relative_to(package_path))
            for path in package_path.glob(glob)]


# The text of the README file
README = (project_folder / "README.md").read_text()

setup(
    name="pcra",
    version=__version__,
    description="Python Create React App",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JennaSys/pcra",
    author="John Sheehan",
    author_email="jennasyseng@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Framework :: Flask",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English"
    ],
    python_requires=">=3.7,<3.8",
    keywords="react material-ui mui transcrypt cli web",
    packages=find_packages(include=["pcra"]),
    package_data={'pcra': [*glob_fix('pcra', 'template/**/*')]},
    install_requires=["patch", "colorama"],
    entry_points={
        "console_scripts": [
            "py-create-react-app=pcra.__main__:main",
        ]
    },
)
