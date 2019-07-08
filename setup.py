from setuptools import setup, find_packages

setup(
  name = "citiesense",
  version = "0.1",
  packages = find_packages(),
  install_requires=[
    'tortilla>=0.5.0',
  ],
  extras_require={
    'dev': [
      'pytest>=4.6.4',
      'vcrpy>=2.0.1',
    ],
  },
)