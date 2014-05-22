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
        make_option('--sheet', action='store', dest='sheet', default=None,
                    help='Sheet name'),
        make_option('--row', action='store', dest='label_row', default=1,
                    help='Location of the row of labels, defaults to 1'),
        make_option('--v', action='store', dest='verbosity', default=0,
                    help='1=Every record; 2=100 records; 3=500 records'),
    )

    def handle(self, *args, **kwargs):
        for filename in args:
            records = transformer.transform(filename, kwargs['sheet'],
                                            kwargs['label_row'])
            verbosity = int(kwargs['verbosity'])
            print "Processing %d records from %s" % (len(records),
                                                     basename(filename))

            to_denormalize = {'organizations': [], 'positions': []}
            records_remaining = len(records)

            for record in records:
                save_for_stats = to_db.save(record)
                to_denormalize = self.add_to_denormalize(save_for_stats,
                                                         to_denormalize)

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

    def add_to_denormalize(self, save_for_stats, to_denormalize):
        for organization in save_for_stats['organizations']:
            if organization not in to_denormalize['organizations']:
                to_denormalize['organizations'].append(organization)

        for position in save_for_stats['positions']:
            if position not in to_denormalize['positions']:
                to_denormalize['positions'].append(position)

        return to_denormalize
