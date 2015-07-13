from setuptools import setup, find_packages

setup(name='gelatin-shot',
      packages=find_packages(),
      scripts=['bin/gelatinshot'],
      install_requires=[
          'Flask'
#          'kerberos>=1.1.1',
#          'Flask-Kerberos',
          ]
     )
