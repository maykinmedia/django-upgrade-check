"""
Provide interfaces to express upgrade constraints.

Upgrades can be constrained by simple (prior) version requirements, management commands
that need to pass or arbitrary callbacks to allow for varying degrees of flexibility
and project-specific checks.

We currently only support SemVer for the version comparisons.
"""

from dataclasses import dataclass

from semantic_version import Version

__all__ = ["VersionRange"]


@dataclass(frozen=True)
class VersionRange:
    """
    Describe a minimum required version and optional upper bound.

    The version range bounds are inclusive. E.g. a range of ``1.0.3 - 1.0.5`` covers
    the versions ``1.0.3``, ``1.0.4`` and ``1.0.5``.
    """

    minimum: str
    """
    The minimum version, typically expressed as major.minor.patch.

    You can specify partial versions like ``1.1`` if the exact patch version is not
    relevant.
    """
    maximum: str = ""
    """
    The upper bound, optional. If unspecified, there is no upper bound.

    If you specify a partial range like ``2.0``, anything newer than ``2.0.0`` will
    be considered out of range.
    """

    def contains(self, in_version: Version):
        min_version = Version.coerce(self.minimum)
        max_version = Version.coerce(self.maximum) if self.maximum else None
        if in_version < min_version:
            return False
        if max_version and in_version > max_version:
            return False
        return True
