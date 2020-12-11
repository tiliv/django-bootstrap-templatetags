# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='django-bootstrap-templatetags',
      version='2.1.3',
      description='Vanilla Bootstrap structures in simple rendering blocks.',
      author='Autumn Valenta',
      author_email='steven@pivotal.energy',
      packages=find_packages(exclude=['test.*', '*test', 'demo*']),
      package_data={'bootstrap_templatetags': ['templates/*/*/*.html']},
      url='https://github.com/pivotal-energy-solutions/django-bootstrap-templatetags',
      license='Apache License 2.0',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Framework :: Django :: 2.1',
          'Framework :: Django :: 2.2',
          'Framework :: Django :: 3.1',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities'
      ],
      python_requires='>=3.4,',
      install_requires=[
          'Django>=2.2',
      ],
      )
