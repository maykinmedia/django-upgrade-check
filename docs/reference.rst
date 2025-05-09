=============
API Reference
=============

Defining checks
===============

Upgrade checks are defined as a mapping of target versions and the checks that must
pass to allow upgrading to said target version. The minimum configuration is specifying
a minimum version that the application must currently be on:

.. code-block:: python

    from upgrade_check import UpgradeCheck, VersionRange

    UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.0.2")),
    }

More advanced use cases may also specify an upper limit or a collection of version
ranges that are allowed. Additionally, you can specify management commands that must
complete without errors:

.. code-block:: python

    from upgrade_check import CommandCheck, UpgradeCheck, VersionRange

    UPGRADE_CHECK_PATHS = {
        "2.0.0": UpgradeCheck(
            VersionRange(minimum="1.0.2"),
            code_checks=[
                CommandCheck("my_management_command", options={"interactive": False}),
            ],
        ),
    }


Available checks
================

.. automodule:: upgrade_check
    :members:

Code checks
===========

Management command checks are built-in specializations of the generic
:class:`upgrade_check.constraints.CodeCheck` protocol. You can define your own custom
code checks and hook them up if desired.

.. autoclass:: upgrade_check.constraints.CodeCheck
    :members:
    :undoc-members:
