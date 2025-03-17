import pytest

from django_upgrade_check.models import Version


@pytest.fixture(autouse=True)
def reset_versions(db):
    """
    Undo the result of ``migrate`` during DB setup.
    """
    Version.objects.all().delete()
