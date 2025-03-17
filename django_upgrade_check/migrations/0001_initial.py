# Generated by Django 4.2.20 on 2025-03-17 19:41

from django.db import migrations, models

import django_upgrade_check.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Version",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "version",
                    models.CharField(
                        editable=False,
                        help_text="The recorded version number.",
                        max_length=100,
                        verbose_name="version",
                    ),
                ),
                (
                    "git_sha",
                    models.CharField(
                        editable=False,
                        help_text="The recorded git commit hash.",
                        max_length=100,
                        verbose_name="git hash",
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text=(
                            "Timestamp reflecting when this version was recorded."
                        ),
                        verbose_name="timestamp",
                    ),
                ),
                (
                    "machine_name",
                    models.CharField(
                        default=django_upgrade_check.models.get_machine_name,
                        editable=False,
                        help_text=(
                            "The host name of the machine this version was recorded on."
                        ),
                        max_length=255,
                        verbose_name="machine name",
                    ),
                ),
            ],
            options={
                "verbose_name": "version",
                "verbose_name_plural": "versions",
                "ordering": ("-timestamp",),
                "indexes": [
                    models.Index(
                        models.OrderBy(models.F("timestamp"), descending=True),
                        name="timestamp_idx",
                    )
                ],
            },
        ),
    ]
