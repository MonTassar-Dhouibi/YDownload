from setuptools import setup

setup(
   name='YDown',
   version='1.0',
   description='A useful module',
   author='YDown',
   py_modules=['downloader'],
   #author_email='foomail@foo.com',
   #packages=['YDown'],  #same as name
   #install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
   scripts=['downloader.py'],
   entry_points={'console_scripts': ['YDown=downloader:main']}
   #   'console_scripts': [
   #       'YDown=downloader.py',
   #   ]
   #}

)
