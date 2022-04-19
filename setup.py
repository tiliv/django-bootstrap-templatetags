# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="django-bootstrap-templatetags",
    version="2.1.12",
    description="Vanilla Bootstrap structures in simple rendering blocks.",
    author="Autumn Valenta",
    author_email="steven@pivotal.energy",
    packages=find_packages(exclude=["demo", "bootstrap_templatetags/test*"]),
    include_package_data=True,
    url="https://github.com/pivotal-energy-solutions/django-bootstrap-templatetags",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License (Proprietary)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9.*",
    install_requires=[
        "django>=3.2",
    ],
)
