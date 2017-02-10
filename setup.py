from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.1.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

all_reqs = ['numpy', 'nose']

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='npywriter',
    version=__version__,
    description='A library for writing arbitrarily large .npy files without having to hold them in memory at once.',
    long_description=long_description,
    license='BSD',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Nicola Montecchio',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='nicola.montecchio@gmail.com'
)
