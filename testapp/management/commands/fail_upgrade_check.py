from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Upgrade test utility, always fails"

    def add_arguments(self, parser):
        parser.add_argument("--fail", action="store_true")

    def handle(self, **options):
        if options["fail"]:
            raise CommandError("Failed")
        else:
            pass
