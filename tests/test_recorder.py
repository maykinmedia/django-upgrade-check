import logging
from io import StringIO

from django.core.management import call_command

import pytest
from django_test_migrations.migrator import Migrator
from django_test_migrations.plan import all_migrations

from upgrade_check.models import Version, get_machine_name
from upgrade_check.recorder import record_current_version


@pytest.mark.django_db
def test_record_without_db_tables(migrator: Migrator, caplog: pytest.LogCaptureFixture):
    # On an empty db we should still be able to run part of the migration plan
    # e.g.
    #
    # manage.py contenttypes 0001_initial
    #
    # should not fail because our Version tables don't exist yet.

    initial_state = migrator.apply_initial_migration(("upgrade_check", None))

    with pytest.raises(LookupError):
        initial_state.apps.get_model("upgrade_check", "Version")

    with caplog.at_level(logging.WARNING):
        assert record_current_version() is None

    assert "django-upgrade-check is not ready" in caplog.text


    # migrator.reset() doesn't seem to work... find last by hand:
    last = all_migrations(app_names=["upgrade_check"])[-1]
    migrator.apply_tested_migration(last.key)

    assert record_current_version() is not None


@pytest.mark.django_db
def test_record_new_version(settings):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert not Version.objects.exists()

    record_current_version()

    version = Version.objects.get()

    assert version.version == "1.2.3"
    assert version.git_sha == "abcd1234"
    assert version.timestamp is not None
    assert version.machine_name != ""
    assert "1.2.3@" in str(version)


@pytest.mark.django_db
def test_record_new_version_debounce(settings, caplog: pytest.LogCaptureFixture):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert record_current_version() is not None

    # recording again in quick succession should debounce
    with caplog.at_level(logging.INFO, logger="upgrade_check.recorder"):
        result = record_current_version()

    machine_name = get_machine_name()
    assert (
        f"Version 1.2.3 was already recorded on machine {machine_name} in the past "
        "3600 seconds."
    ) in caplog.text

    assert result is None
    assert Version.objects.count() == 1


@pytest.mark.django_db
def test_record_new_version_no_debounce_different_version(settings):
    settings.RELEASE = "1.2.3"
    settings.GIT_SHA = "abcd1234"
    assert record_current_version() is not None

    settings.RELEASE = "2.3.0"
    result = record_current_version()

    assert result is not None
    assert Version.objects.count() == 2


@pytest.mark.django_db
def test_migrate_records_version(settings):
    settings.RELEASE = "1.2.3"
    assert not Version.objects.exists()

    call_command("migrate", stdout=StringIO(), stderr=StringIO(), verbosity=0)

    version = Version.objects.get()
    assert version.version == "1.2.3"
