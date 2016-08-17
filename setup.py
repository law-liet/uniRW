from distutils.core import setup

setup(
  name = 'uniRW',
  packages = ['uniRW', 'uniRW/deprecated'],
  version = '0.4.8',
  description = 'A universal reader and writer for stateful data file processing',
  author = 'Langxuan Su',
  author_email = 'lawliet@orion.codes',
  url = 'https://github.com/law-liet/uniRW',
  download_url = 'https://github.com/law-liet/uniRW/tarball/v0.4.8',
  keywords = ['declarative', 'functional', 'reusable', 'universal', 'stateful', 'data',
              'file', 'processing', 'csv', 'reader', 'writer',  'map', 'reduce', 'filter'],
  classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Text Processing",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
