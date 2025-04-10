

Welcome to django-upgrade-check's documentation!
================================================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/django-upgrade-check
:Keywords: ``<keywords>``
:PythonVersion: 3.10

|build-status| |code-quality| |black| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Integrate project upgrade checks in Django's system check framework.

.. contents::

.. section-numbering::

Features
========

* Define supported upgrade paths in settings using Semantic Versioning.
* Integrates with Django's system check framework, preventing migrations from running
  on invalid upgrade paths.
* Planned: run management commands as part of a check.
* Planned: hook up your own checks as simple python functions.
* Battle-tested and doesn't get in the way during development.

Installation and usage
======================

See the `documentation <https://django-upgrade-check.readthedocs.io/>`_ on ReadTheDocs
or check the ``docs`` folder.

Local development
=================

To install and develop the library locally, use:

.. code-block:: bash

    pip install -e .[tests,coverage,docs,release]

When running management commands via ``django-admin``, make sure to add the root
directory to the python path (or use ``python -m django <command>``):

.. code-block:: bash

    export PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=testapp.settings
    django-admin check
    # or other commands like:
    # django-admin makemessages -l nl


.. |build-status| image:: https://github.com/maykinmedia/django-upgrade-check/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-upgrade-check/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/django-upgrade-check/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/django-upgrade-check/actions?query=workflow%3A%22Code+quality+checks%22

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. |coverage| image:: https://codecov.io/gh/maykinmedia/django-upgrade-check/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-upgrade-check
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-upgrade-check/badge/?version=latest
    :target: https://django-upgrade-check.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-upgrade-check.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-upgrade-check.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-upgrade-check.svg
    :target: https://pypi.org/project/django-upgrade-check/
