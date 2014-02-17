import sys

from django.core.management.base import BaseCommand
from optparse import make_option
from os.path import basename

from ...utils import to_db, transformer


# TODO: Display help if unable to transform a file
# TODO: Switch to logging rather than direct output
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sheet', action='store', dest='sheet', default=None,
                    help='Sheet name'),
        make_option('--file', action='store', dest='filename', default=None,
                    help='File location'),
        make_option('--v', action='store', dest='verbosity', default=0,
                    help='File location'),
    )

    def handle(self, filename=None, sheet=None, verbosity=0, *args, **kwargs):
        if filename is None:
            sys.stderr.write('Must provide at least one file to process')
            return

        records = transformer.transform(filename, sheet)
        if verbosity >= 2:
            print "Processing %d records from %s" % (len(records),
                    basename(filename))
        for record in records:
            to_db.save(record)
            if verbosity >= 2:
                sys.stdout.write('.')
                sys.stdout.flush()

        if verbosity >= 2:
            sys.stdout.write('\n')
            sys.stdout.flush()
