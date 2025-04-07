"""
Provide interfaces to express upgrade constraints.

Upgrades can be constrained by simple (prior) version requirements, management commands
that need to pass or arbitrary callbacks to allow for varying degrees of flexibility
and project-specific checks.

We currently only support SemVer for the version comparisons.
"""

from collections.abc import Collection
from dataclasses import dataclass, field

from semantic_version import Version

__all__ = ["VersionRange", "UpgradeCheck"]


@dataclass(slots=True, unsafe_hash=True)
class VersionRange:
    """
    Describe a minimum required version and optional upper bound.

    The version range bounds are inclusive. E.g. a range of ``1.0.3 - 1.0.5`` covers
    the versions ``1.0.3``, ``1.0.4`` and ``1.0.5``.

    ``VersionRange`` instances are intended to be immutable.
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
    _min_version: Version = field(init=False)
    _max_version: Version | None = field(init=False)

    def __post_init__(self):
        self._min_version = Version.coerce(self.minimum)
        self._max_version = Version.coerce(self.maximum) if self.maximum else None

    def contains(self, in_version: Version):
        if in_version < self._min_version:
            return False
        if self._max_version and in_version > self._max_version:
            return False
        return True


class UpgradeCheck:
    """
    Define the conditions for a valid upgrade check.

    Provide either a :class:`VersionRange` or a collection of version ranges to test if
    this check passes. The version number check passes as soon as one range satisfies
    the provided version.

    .. todo:: support management command checks
    .. todo:: support arbitrary callables/callbacks for additional (script) checks
    """

    valid_ranges: Collection[VersionRange]

    def __init__(
        self,
        valid_range: VersionRange | Collection[VersionRange],
    ):
        # normalize to a collection
        self.valid_ranges = (
            (valid_range,) if isinstance(valid_range, VersionRange) else valid_range
        )

    def check_version(self, current_version: Version) -> bool:
        """
        Check if the provided version is contained in any of the valid ranges.

        :arg current_version: The version the application is currently at.
        """
        for version_range in self.valid_ranges:
            if version_range.contains(current_version):
                return True
        return False
