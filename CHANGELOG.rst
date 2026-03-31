=========
Changelog
=========

2.0.0 (unreleased)
==================

Maintenance and bugfix release.

**Breaking changes**

* Dropped Django 4.2 support.
* Constraint ``non_empty_version`` is now enforced, existing installations should make sure no empty `Version` objects
  are present.

**Features**

* [#5] Added Django 6 support.

**Bugfixes**

* Fixed incorrect constraint initialization in ``Version`` model.

1.0.0 (2025-04-10)
==================

Feature release, Django-upgrade-check is now feature complete.

**Features**

* Added ability to run code checks.
* Added management command checks as built-in code check.

0.2.0 (2025-04-10)
==================

Initial preview release.

The package is extracted from Open Formulieren and published as re-usable library now.

**Features**

* Record deployed version(s) on post-migrate.
* Check (new) version against latest deployed version and upgrade check configuration.
* Ability to define valid upgrade paths in settings.
* Automatic system checks that prevent database mutations on invalid upgrade paths.

Currently missing features:

* Running management commands in checks
* Running project-specific check scripts
