from setuptools import setup, find_packages

setup(name='gelatin-shot',
      version = '0.1',
      packages=find_packages(),
      scripts=['bin/gelatinshot'],
      install_requires=[
          'Flask',
          'SQLAlchemy',
          'simplejson',
          'psycopg2',
#          'kerberos>=1.1.1',
#          'Flask-Kerberos',
          ],
     )
