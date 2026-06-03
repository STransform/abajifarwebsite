from pathlib import Path

import polib
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Compile locale .po files to .mo files using polib, without GNU gettext."

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--locale",
            action="append",
            dest="locales",
            help="Locale code to compile, for example ax or ox. Can be used multiple times.",
        )

    def handle(self, *args, **options):
        locale_roots = [Path(path) for path in getattr(settings, "LOCALE_PATHS", [])]
        if not locale_roots:
            locale_roots = [Path(settings.BASE_DIR) / "locale"]

        requested_locales = set(options.get("locales") or [])
        compiled = 0

        for locale_root in locale_roots:
            if not locale_root.exists():
                continue

            po_files = locale_root.glob("*/LC_MESSAGES/*.po")
            for po_file in po_files:
                locale_code = po_file.parent.parent.name
                if requested_locales and locale_code not in requested_locales:
                    continue

                mo_file = po_file.with_suffix(".mo")
                try:
                    polib.pofile(str(po_file)).save_as_mofile(str(mo_file))
                except Exception as exc:
                    raise CommandError(f"Could not compile {po_file}: {exc}") from exc

                compiled += 1
                self.stdout.write(self.style.SUCCESS(f"Compiled {po_file} -> {mo_file}"))

        if compiled == 0:
            self.stdout.write(self.style.WARNING("No .po files found to compile."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Compiled {compiled} message file(s)."))
