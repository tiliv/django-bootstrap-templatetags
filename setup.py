# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='django-bootstrap-templatetags',
      version='1.0',
      description='Vanilla Bootstrap structures in simple rendering blocks.',
      author='Tim Valenta',
      author_email='tim.valenta@thesimpler.net',
      packages=find_packages(),
      url='https://github.com/tiliv/django-bootstrap-templatetags',
      license='Apache License 2.0',
      classifiers=[
           'Environment :: Web Environment',
           'Framework :: Django',
           'Intended Audience :: Developers',
           'Operating System :: OS Independent',
           'Programming Language :: Python',
           'Topic :: Software Development',
           'License :: OSI Approved :: Apache Software License',
      ],
      requires=['django (>=1.2)'],
      dependency_links=['git+https://github.com/tiliv/django-easytag'],
)
