from setuptools import setup, find_packages

setup(name='monopoly_sim',
      version='0.0.11',
      description='A monopoly game simulator',
      install_requires=['setuptools>=4.0.1'],
      url='https://github.com/HaywardPeirce/monopoly-sim',
      packages = find_packages(),
      py_modules = ['monopoly_sim.monopoly'],
      include_package_data=True,
      #package_data={'monopoly-sim': ['properties.json', 'places.json']}
      #data_files   = [ ("monopoly-sim",  ['properties.json', 'places.json'])]
     )