import pytest
from semantic_version import Version

from django_upgrade_check.constraints import UpgradeCheck, VersionRange


@pytest.mark.parametrize(
    "minimum,maximum,test,expected_result",
    [
        # no maximum version
        ("1.0.0", "", "1.0.0", True),
        ("1.0.0", "", "1.1.0", True),
        ("1.0.0", "", "1.0.1", True),
        ("1.0.0", "", "2.0.0", True),
        ("1.0", "", "2.0.0", True),
        ("1", "", "2.0.0", True),
        ("1.0.0", "", "0.99", False),
        ("1.1", "", "0.99", False),
        ("1", "", "0.99", False),
        ("2.0.3", "", "2.0.2", False),
        # with maximum version
        ("1.0.0", "1.1.0", "1.0.0", True),
        ("1.0.0", "1.1.0", "1.1.0", True),
        ("1.0.0", "1.1.0", "1.1.1", False),
        ("1.0.0", "1.1.0", "2.0.0", False),
        ("1.0.0", "2", "1.5.10", True),
        ("1.0.0", "2", "2.0.0", True),
        ("1.0.0", "2", "2.0.1", False),
        ("1.0.0", "2", "2.1.0", False),
        ("1.0.0", "2", "3.0.0", False),
        # unspecified patch
        ("2.1", "", "2.1.0", True),
        ("2.1", "", "2.1.3", True),
        ("2.1", "", "2.0.999", False),
        # unspecified minor
        ("2", "", "2.0.0", True),
        ("2", "", "1.0.0", False),
        ("2", "", "2.1.0", True),
    ],
)
def test_containment(minimum: str, maximum: str, test: str, expected_result: bool):
    version_range = VersionRange(minimum=minimum, maximum=maximum)

    result = version_range.contains(Version.coerce(test))

    assert result == expected_result


@pytest.mark.parametrize(
    "test_version,expected",
    [
        ("1.0.0", False),
        ("1.1.2", False),
        ("1.1.3", True),
        ("1.2.0", True),
        ("2.0.0", True),
        ("2.0.1", False),
        ("2.1.0", False),
    ],
)
def test_ugprade_check_single_range(test_version: str, expected: bool):
    check = UpgradeCheck(valid_range=VersionRange(minimum="1.1.3", maximum="2.0.0"))
    current_version = Version(test_version)

    result = check.check_version(current_version)

    assert result == expected


@pytest.mark.parametrize(
    "test_version,expected",
    [
        ("1.0.0", False),
        ("1.1.2", False),
        ("1.1.3", True),
        ("1.1.5", True),
        ("1.1.6", False),
        ("1.2.0", True),
        ("2.0.0", True),
        ("2.0.1", False),
        ("2.1.0", False),
    ],
)
def test_ugprade_check_multiple_ranges(test_version: str, expected: bool):
    check = UpgradeCheck(
        valid_range={
            VersionRange(minimum="1.1.3", maximum="1.1.5"),
            VersionRange(minimum="1.2.0", maximum="2.0.0"),
        }
    )
    current_version = Version(test_version)

    result = check.check_version(current_version)

    assert result == expected
