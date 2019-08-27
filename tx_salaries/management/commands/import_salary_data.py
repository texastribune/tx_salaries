import sys

from django.core.management import BaseCommand, CommandError

from os.path import basename

from ...utils import to_db, transformer
from ... import models

import requests


def out(s):
    sys.stdout.write(s)
    sys.stdout.flush()


# TODO: Display help if unable to transform a file
# TODO: Switch to logging rather than direct output
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'filename',
            nargs='*',
        )
        parser.add_argument(
            '-f', '--fetch',
            action='store',
            dest='fetch',
            default=None,
            help='Fetch the S3 URL of given transformer',
        )
        parser.add_argument(
            '-s', '--sheet',
            action='store',
            dest='sheet',
            default=None,
            help='Sheet name',
        )
        parser.add_argument(
            '-r', '--row',
            action='store',
            dest='label_row',
            default=1,
            help='Location of the row of labels, defaults to 1',
        )
        parser.add_argument(
            '--skip-infer-types',
            action='store_false',
            default=True,
        )

    def download_file(self, url, filename):
        req = requests.get(url, stream=True)

        with open(filename, 'wb') as fo:
            for chunk in req.iter_content(1024):
                if chunk:
                    fo.write(chunk)
                    fo.flush()

    def fetch_file(self, **options):
        import importlib
        from os import system

        # Convert file path to module path
        transformer_path = 'tx_salaries.utils.transformers.' + options['fetch']
        transformer_file = importlib.import_module(transformer_path)

        # Fetch url string from transformer file
        url = transformer_file.TransformedRecord.URL
        filename = basename(url)

        # Download file
        self.download_file(url, filename)

        self.import_file(filename, **options)
        # Remove downloaded file
        system('rm %s' % filename)

    def handle(self, *args, **options):
        if options['fetch']:
            self.fetch_file(**options)
        else:
            files = options['filename']

            if not files:
                raise CommandError('No filename(s) provided')

            for f in files:
                self.import_file(f, **options)

    def import_file(self, f, **options):
        sheet = options['sheet']
        label_row = options['label_row']
        skip_infer_types = options['skip_infer_types']

        records, warnings = transformer.transform(
            f,
            sheet,
            label_row,
            infer_types=skip_infer_types,
        )

        all_orgs = set([i['tx_people.Organization']['name'] for i in records])

        existing_orgs = models.Organization.objects.filter(
            name__in=all_orgs,
            parent=None)

        if existing_orgs:
            self.stdout.write('The following organizations '
                              'already exist in the database:')

            for org in existing_orgs:
                self.stdout.write(org.name)

            reply = raw_input('In order to update, everything currently in '
                              'the database concerning these organizations '
                              'must be deleted. Do you want to continue? '
                              '(Y/n): ').lower().strip()

            if reply[0] == 'n':
                self.stdout.write('Stopping. Did not touch anything.')
                return

            if reply[0] == 'y':
                self.stdout.write('Deleting organizations...')
                existing_orgs.delete()
                self.stdout.write('Done! Moving on.')

        verbosity = options['verbosity']

        self.stdout.write(
            'Processing {} records from {}'.format(
                len(records),
                basename(f),
            )
        )

        to_denormalize = {
            'organizations': set(),
            'positions': set(),
            'date_provided': records[0]['date_provided'],
        }

        records_remaining = len(records)

        for record in records:
            save_for_stats = to_db.save(record)

            to_denormalize['organizations'].update(
                save_for_stats['organizations'],
            )
            to_denormalize['positions'].update(
                save_for_stats['positions'],
            )

            records_remaining -= 1

            if verbosity == 1 and records_remaining % 500 == 0:
                self.stdout.write(
                    '{0} records remaining'.format(
                        records_remaining
                    )
                )
            elif verbosity == 2 and records_remaining % 100 == 0:
                self.stdout.write(
                    '{0} records remaining'.format(
                        records_remaining
                    )
                )
            elif verbosity == 3:
                self.stdout.write('.', ending='')
                self.stdout.flush()

        self.stdout.write('')

        to_db.denormalize(to_denormalize)

        for warning in warnings:
            self.stdout.write(warning)
