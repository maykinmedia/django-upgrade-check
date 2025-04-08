from django.conf import settings

from .constraints import (
    InvalidVersionError,
    TargetVersionMatchError,
    UpgradePaths,
    check_upgrade_possible,
)
from .models import Version
from .recorder import get_version_info


class UpgradeBlocked(Exception):
    def __init__(self, reason: str, *args, **kwargs):
        super().__init__(reason, *args, **kwargs)
        self.reason = reason


def _get_valid_upgrade_paths() -> UpgradePaths:
    paths = getattr(settings, "UPGRADE_CHECK_PATHS", {})
    return paths


def run_upgrade_check():
    """
    Gather the current and last recorded project versions and check any upgrades.

    The current version is taken from the code and interpreted as the "target version"
    to upgrade to. That *may* be the currently active version. The last recorded
    project version is taken from the database - we simply take the last recorded entry
    and deliberately don't do any additional timestamp checks or filtering to account
    for possible (small) clock drifts.

    :raises UpgradeBlocked: if upgrading is not possible due to the constraints.
    """
    most_recent_recorded_version = Version.objects.order_by("-timestamp").first()
    # if we have no version history, any version can be deployed -> check passes
    if most_recent_recorded_version is None:
        return

    current: str = most_recent_recorded_version.version
    target = get_version_info()[0]
    strict: bool = getattr(settings, "UPGRADE_CHECK_STRICT", False)

    err_msg = (
        f"Upgrading from {current} to {target} is not possible (strict "
        f"checks: {'yes' if strict else 'no'})."
    )
    try:
        upgrade_possible = check_upgrade_possible(
            _get_valid_upgrade_paths(),
            from_version=current,
            to_version=target,
            raise_if_no_match=strict,
        )
    except InvalidVersionError as exc:
        if strict:
            raise UpgradeBlocked("Invalid semver version provided.") from exc
        else:
            return
    except TargetVersionMatchError as exc:
        raise UpgradeBlocked(err_msg) from exc

    if not upgrade_possible:
        raise UpgradeBlocked(err_msg)
