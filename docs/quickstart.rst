==========
Quickstart
==========

Installation
============

Install from PyPI with pip or compatible package managers:

.. code-block:: bash

    pip install django-upgrade-check

And add the app to the installed apps:

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        "upgrade_check",
        ...
    ]


Next, ensure the following settings are defined in your project:

``settings.RELEASE``
    The version number of the code, e.g. ``"1.0.3"``. If it's not a semnver version
    (e.g. ``dev`` in develoment), upgrade checks are skipped.

``settings.GIT_SHA``
    The commit hash matching this version. Required, but can be any string - it's only
    recorded for historical reasons.

``settings.UPGRADE_CHECK_PATHS``
    A dictionary mapping the upgrade target version to the upgrade check configuration.
    For example:

    .. code-block:: python

        UPGRADE_CHECK_PATHS = {
            "2.0": UpgradeCheck(VersionRange(minimum="1.0")),
        }

    Versions are matched using the ``~=`` spec, e.g. ``"2.0"`` in the example will match
    ``"2.0.0"``, ``"2.0"`` and any ``"2.0.x"`` patch release.

``settings.UPGRADE_CHECK_STRICT``
    Default ``False`` - in strict mode, if ``settings.RELEASE`` cannot be matched to any
    target version in ``settings.UPGRADE_CHECK_PATHS``, the upgrade check will fail and
    block the upgrade. In develoment with strict mode, warnings will be emitted that are
    otherwise silencded.

Finally, run migrate to create the necessary database tables:

.. code-block:: bash

    python manage.py migrate

Usage
=====

You're all set! As long as ``settings.RELEASE`` accurately reflects the new version
being deployed, and you manage ``settings.UPGRADE_CHECK_STRICT``, the library takes it
from there:

* on invalid upgrade paths, the systme check errors out
* because migrations (by default) run system checks before migrating, this prevents
  your database from being modified
