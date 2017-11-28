import sys

from django.core.management.base import BaseCommand
# from argparse import add_argument
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
        parser.add_argument('filename')

        parser.add_argument('--fetch',
                            action='store',
                            dest='fetch',
                            default=None,
                            help='Fetch the s3 url of given transformer')
        parser.add_argument('--sheet',
                            action='store',
                            dest='sheet',
                            default=None,
                            help='Sheet name')
        parser.add_argument('--row',
                            action='store',
                            dest='label_row',
                            default=1,
                            help='Location of the row of labels, defaults to 1')
        parser.add_argument('--v',
                            action='store',
                            dest='verbosity',
                            default=0,
                            help='1=Every record; 2=100 records; 3=500 records')
        parser.add_argument('--skip-infer-types',
                            action='store_false',
                            default=True)

    # option_list = BaseCommand.option_list + (
    #     make_option('--fetch', action='store', dest='fetch', default=None,
    #                 help='Fetch the s3 url of given transformer'),
    #     make_option('--sheet', action='store', dest='sheet', default=None,
    #                 help='Sheet name'),
    #     make_option('--row', action='store', dest='label_row', default=1,
    #                 help='Location of the row of labels, defaults to 1'),
    #     make_option('--v', action='store', dest='verbosity', default=0,
    #                 help='1=Every record; 2=100 records; 3=500 records'),
    #     make_option('--skip-infer-types', action='store_false', default=True),
    # )

    def download_file(self, url, **options):
        req = requests.get(url, stream=True)
        filename = options['filename']
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

        self.import_file(**options)
        # Remove downloaded file
        system('rm %s' % filename)

    def handle(self, *args, **options):
        if options['fetch']:
            file = options['fetch']
            self.fetch_file(file, **options)
        else:
            files = options['filename']
            # filename = self.import_file(file, **options)
            for file in files:
                self.import_file(file, **options)

    def import_file(self, *args, **options):
        if options['sheet']:
            sheet = options['sheet']
        else:
            sheet = None

        if options['label_row']:
            label_row = options['label_row']
        else:
            label_row = 1

        if options['skip_infer_types']:
            skip_infer_types = options['skip_infer_types']
        else:
            skip_infer_types = True

        filename = options['filename']

        records, warnings = transformer.transform(
            filename, sheet, label_row,
            infer_types=skip_infer_types)

        verbosity = int(options['verbosity'])

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

        self.stdout.write('Processing {} records from {}'.format(
            len(records), basename(filename)))

        to_denormalize = {'organizations': set(), 'positions': set(),
                          'date_provided': records[0]['date_provided']}
        records_remaining = len(records)

        for record in records:
            save_for_stats = to_db.save(record)

            to_denormalize['organizations'].update(
                save_for_stats['organizations'])
            to_denormalize['positions'].update(
                save_for_stats['positions'])

            records_remaining -= 1
            if verbosity == 1:
                out('.')
            elif verbosity == 2 and records_remaining % 100 == 0:
                print "%s records remaining" % records_remaining
            elif verbosity >= 3 and records_remaining % 500 == 0:
                print "%s records remaining" % records_remaining

        if verbosity == 1:
            out('\n')

        to_db.denormalize(to_denormalize)

        for warning in warnings:
            self.stdout.write(warning)
