import sys

from django.core.management.base import BaseCommand
from optparse import make_option
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
    option_list = BaseCommand.option_list + (
        make_option('--fetch', action='store', dest='fetch', default=None,
                    help='Fetch the s3 url of given transformer'),
        make_option('--sheet', action='store', dest='sheet', default=None,
                    help='Sheet name'),
        make_option('--row', action='store', dest='label_row', default=1,
                    help='Location of the row of labels, defaults to 1'),
        make_option('--v', action='store', dest='verbosity', default=0,
                    help='1=Every record; 2=100 records; 3=500 records'),
    )

    def download_file(self, url, filename):
        req = requests.get(url, stream=True)

        with open(filename, 'wb') as fo:
            for chunk in req.iter_content(1024):
                if chunk:
                    fo.write(chunk)
                    fo.flush()

    def fetch_file(self, **kwargs):
        import importlib
        from os import system

        # Convert file path to module path
        transformer_path = 'tx_salaries.utils.transformers.' + kwargs['fetch']
        transformer_file = importlib.import_module(transformer_path)

        # Fetch url string from transformer file
        url = transformer_file.TransformedRecord.URL
        filename = basename(url)

        # Download file
        self.download_file(url, filename)

        self.import_file(filename, **kwargs)
        # Remove downloaded file
        system('rm %s' % filename)

    def handle(self, *args, **kwargs):
        if kwargs['fetch']:
            filename = self.fetch_file(**kwargs)

        for filename in args:
            self.import_file(filename, **kwargs)

    def import_file(self, filename, **kwargs):
        records = transformer.transform(filename, kwargs['sheet'],
                                        kwargs['label_row'])
        verbosity = int(kwargs['verbosity'])

        all_orgs = set([i['tx_people.Organization']['name'] for i in records])

        existing_orgs = models.Organization.objects.filter(
            name__in=all_orgs,
            parent=None)

        if existing_orgs:

            self.stdout.write('The following organizations '
                              'already exist in the database:')

            for org in existing_orgs:
                self.stdout.write(org.name)

            reply_invalid = True

            while (reply_invalid):
                reply = raw_input('In order to update, everything currently in '
                                  'the database concerning these organizations '
                                  'must be deleted. Do you want to continue? '
                                  '(Y/n): ').lower().strip()
                if reply[0].lower() == 'n' or reply[0].lower() == 'y':
                    reply_invalid = False
                    if reply[0].lower() == 'n':
                        self.stdout.write('Stopping. Did not touch anything.')
                        return
                    if reply[0].lower() == 'y':
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
