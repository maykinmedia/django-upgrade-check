import pytest

from django_upgrade_check.constraints import UpgradeCheck, UpgradePaths, VersionRange
from django_upgrade_check.models import Version
from django_upgrade_check.upgrade_checks import UpgradeBlocked, run_upgrade_check

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def upgrade_setting(settings):
    paths: UpgradePaths = {
        "3.0": UpgradeCheck(VersionRange(minimum="2.1")),
        "2.0.0": UpgradeCheck(VersionRange(minimum="1.1")),
        "1.2": UpgradeCheck(VersionRange(minimum="1.1", maximum="1.1.99")),
    }
    settings.UPGRADE_CHECK_PATHS = paths


def test_upgrade_check_upgrade_blocked(settings):
    # upgrade from 1.0 -> 1.2.2
    settings.RELEASE = "1.2.2"
    settings.GIT_SHA = "abcd1234"
    Version.objects.create(version="1.0.0", git_sha="dummy")

    with pytest.raises(UpgradeBlocked):
        run_upgrade_check()


def test_upgrade_check_upgrade_ok(settings):
    # upgrade from 1.3.4 -> 2.0.3
    settings.RELEASE = "2.0.3"
    settings.GIT_SHA = "abcd1234"
    Version.objects.create(version="1.3.4", git_sha="dummy")

    try:
        run_upgrade_check()
    except UpgradeBlocked:
        pytest.fail("Upgrade check should pass")


def test_upgrade_check_no_prior_history_upgrade_ok(settings):
    # install fresh instance at 2.0.3
    settings.RELEASE = "2.0.3"
    settings.GIT_SHA = "abcd1234"
    assert not Version.objects.exists()

    try:
        run_upgrade_check()
    except UpgradeBlocked:
        pytest.fail("Upgrade check should pass")


def test_upgrade_check_undefined_target_version_with_lax_checks(settings):
    settings.RELEASE = "4.0.0"
    settings.GIT_SHA = "abcd1234"
    Version.objects.create(version="1.3.4", git_sha="dummy")

    try:
        run_upgrade_check()
    except UpgradeBlocked:
        pytest.fail("Upgrade check should pass")


def test_upgrade_check_undefined_target_version_with_strict_checks(settings):
    settings.RELEASE = "4.0.0"
    settings.GIT_SHA = "abcd1234"
    settings.UPGRADE_CHECK_STRICT = True
    Version.objects.create(version="1.3.4", git_sha="dummy")

    with pytest.raises(UpgradeBlocked):
        run_upgrade_check()


@pytest.mark.parametrize(
    "target_version",
    [
        "latest",
        "dev",
        "",
    ],
)
def test_upgrade_check_non_semver_block_in_strict_mode(settings, target_version: str):
    settings.RELEASE = target_version
    settings.GIT_SHA = "abcd1234"
    settings.UPGRADE_CHECK_STRICT = True
    Version.objects.create(version="1.3.4", git_sha="dummy")

    with pytest.raises(UpgradeBlocked):
        run_upgrade_check()


@pytest.mark.parametrize(
    "current_version",
    [
        "latest",
        "dev",
        "",
    ],
)
def test_upgrade_check_non_semver_current_block_in_strict_mode(
    settings, current_version: str
):
    settings.RELEASE = "2.0.0"
    settings.GIT_SHA = "abcd1234"
    settings.UPGRADE_CHECK_STRICT = True
    Version.objects.create(version=current_version, git_sha="dummy")

    with pytest.raises(UpgradeBlocked):
        run_upgrade_check()


@pytest.mark.parametrize(
    "target_version",
    [
        "latest",
        "dev",
        "",
    ],
)
def test_upgrade_check_non_semver_dont_block_in_lax_mode(settings, target_version: str):
    settings.RELEASE = target_version
    settings.GIT_SHA = "abcd1234"
    settings.UPGRADE_CHECK_STRICT = False
    Version.objects.create(version="1.3.4", git_sha="dummy")

    try:
        run_upgrade_check()
    except UpgradeBlocked:
        pytest.fail("Upgrade check should pass")


@pytest.mark.parametrize(
    "current_version",
    [
        "latest",
        "dev",
        "",
    ],
)
def test_upgrade_check_non_semver__current_dont_block_in_lax_mode(
    settings, current_version: str
):
    settings.RELEASE = "2.0.0"
    settings.GIT_SHA = "abcd1234"
    settings.UPGRADE_CHECK_STRICT = False
    Version.objects.create(version=current_version, git_sha="dummy")

    try:
        run_upgrade_check()
    except UpgradeBlocked:
        pytest.fail("Upgrade check should pass")
