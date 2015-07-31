from setuptools import setup, find_packages

setup(name='gelatinshot',
      version = '0.1',
      packages=['gelatinshot'],
      package_dir={'gelatinshot': 'bin'},
      py_modules = ['bin/gelatinshot'],
      install_requires=[
          'Flask',
          'SQLAlchemy',
          'simplejson',
          'psycopg2',
          'kerberos==1.1.1',
          'Flask-Kerberos',
          'requests-kerberos'
          ],
     )
