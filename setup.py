# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='django-bootstrap-templatetags',
      version='2.0.0',
      description='Vanilla Bootstrap structures in simple rendering blocks.',
      author='Autumn Valenta',
      author_email='steven@pivotal.energy',
      packages=find_packages(exclude=["*test.*", "*test", "demo*"]),
      package_data={'bootstrap_templatetags': ['templates/*/*/*.html']},
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
