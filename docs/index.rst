.. django-upgrade-check documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-upgrade-check's documentation!
================================================

|build-status| |code-quality| |ruff| |coverage| |docs|

|python-versions| |django-versions| |pypi-version|

Integrate project upgrade checks in Django's system check framework.

Imagine you keep improving you Django project and you share this to the world with new
releases. Sooner or later, you will run into some situation where upgrading an existing
instance goes horribly wrong because they're updating from a version you did not
anticipate or account for. Or, you did account for it and put it in the release notes,
but people skipped over those.

You can avoid the support nightmare created in such situations by leveraging adding
django-upgrade-check to your project and then express which (minimum) versions are
required before you can upgrade to a newer version. If the check doesn't pass, nothing
is lost - the instance code can be downgraded again and you don't have to worry about
rolling back database migrations.

.. note:: We only support semantic versioning. If you use a different versioning scheme,
   this package is unfortunately not suitable for your needs.

Features
========

* Define supported upgrade paths in settings using Semantic Versioning.
* Integrates with Django's system check framework, preventing migrations from running
  on invalid upgrade paths.
* Planned: run management commands as part of a check.
* Planned: hook up your own checks as simple python functions.
* Battle-tested and doesn't get in the way during development.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   changelog


Credits
=======

Django-upgrade-check was originally part of the
`Open Formulieren <http://github.com/open-formulieren/open-forms>`_ project. We wanted
to be able to squash migrations and not have to maintain certain data migrations until
the end of days, while still providing strong guarantees for (production) instances.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |build-status| image:: https://github.com/maykinmedia/django-upgrade-check/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/django-upgrade-check/actions?query=workflow%3A%22Run+CI%22

.. |code-quality| image:: https://github.com/maykinmedia/django-upgrade-check/workflows/Code%20quality%20checks/badge.svg
     :alt: Code quality checks
     :target: https://github.com/maykinmedia/django-upgrade-check/actions?query=workflow%3A%22Code+quality+checks%22

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

.. |coverage| image:: https://codecov.io/gh/maykinmedia/django-upgrade-check/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/django-upgrade-check
    :alt: Coverage status

.. |docs| image:: https://readthedocs.org/projects/django-upgrade-check/badge/?version=latest
    :target: https://django-upgrade-check.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/django-upgrade-check.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/django-upgrade-check.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-upgrade-check.svg
    :target: https://pypi.org/project/django-upgrade-check/
