import sys

from django.core.management.base import BaseCommand
from optparse import make_option
from os.path import basename

from ...utils import to_db, transformer


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
        system('curl %s -o %s' % (url, filename))

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
        print "Processing %d records from %s" % (len(records),
                                                 basename(filename))

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
