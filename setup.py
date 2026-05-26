
import os

from setuptools import setup, find_packages

DESCRIPTION = (
    "Community-maintained fork of bauh focused on modern Linux compatibility"
)

AUTHOR = "Vinicius Moreira"
AUTHOR_EMAIL = "vinicius_fmoreira@hotmail.com"
DIST_NAME = 'bearhub'
APP_PACKAGE = 'bauh'
URL = "https://github.com/spalencsar/" + DIST_NAME

file_dir = os.path.dirname(os.path.abspath(__file__))

if os.getenv('BAUH_SETUP_NO_REQS'):
    requirements = []
else:
    with open(f'{file_dir}/requirements.txt', 'r') as f:
        requirements = [line.strip() for line in f.readlines() if line]


with open(file_dir + '/{}/__init__.py'.format(APP_PACKAGE), 'r') as f:
    exec(f.readlines()[0])


setup(
    name=DIST_NAME,
    version=eval('__version__'),
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    python_requires=">=3.5",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={APP_PACKAGE: ["view/resources/locale/*", "view/resources/img/*", "view/resources/style/*", 'view/resources/style/*/img/*', "gems/*/resources/img/*", "gems/*/resources/locale/*", "desktop/*"]},
    install_requires=requirements,
    test_suite="tests",
    entry_points={
        "console_scripts": [
            "bearhub=bauh.app:main",
            "bearhub-tray=bauh.app:tray",
            "bearhub-cli=bauh.cli.app:main"
        ]
    },
    include_package_data=True,
    license="zlib/libpng",
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
