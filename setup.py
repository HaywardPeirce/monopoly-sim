from setuptools import setup, find_packages

setup(name='monopoly-sim',
      version='0.0.5',
      description='A monopoly game simulator',
      install_requires=['setuptools>=4.0.1'],
      url='https://github.com/HaywardPeirce/monopoly-sim',
      py_modules = ['monopoly'],
      #include_package_data=True,
      package_data={
        '': ['properties.json', 'places.json']
      }
     )