from setuptools import setup

setup(name='gitlabcpc',
      version='0.1',
      description='cross projects gitlab cli tool',
      url='https://github.com/CloudInn/gitlabcpc',
      author='Abdelrahman Ghareeb',
      author_email='abdelrahman@slashproc.net',
      license='GPL3',
      install_requires=['python-gitlab', 'cement', 'pyspin', 'tabulate'],
      zip_safe=False)
