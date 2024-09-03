import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.17'
PACKAGE_NAME = 'python-isodata'
AUTHOR = 'Caffeine Lab, LLC.'
AUTHOR_EMAIL = 'glenn@caffeinelab.com'
URL = 'https://github.com/CaffeineLab/isodata'

LICENSE = 'GNU General Public License v3.0'
DESCRIPTION = 'Energy Market downloading tools'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'loguru',
      'requests',
      'python-dateutil',
      'tenacity',
      'lxml'
]


setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      )
