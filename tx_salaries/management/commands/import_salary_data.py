from os.path import basename
import sys

from django.core.management.base import BaseCommand

from ...utils import to_db, transformer


# TODO: Display help if unable to transform a file
# TODO: Switch to logging rather than direct output
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        verbosity = kwargs.get('verbosity', 1)
        if len(args) is 0:
            sys.stderr.write('Must provide at least one file to process')
            return

        if verbosity >= 2:
            print "Number of file(s) to process: {num_of_files}".format(
                    num_of_files=len(args))
        for filename in args:
            records = transformer.transform(filename)
            if verbosity >= 2:
                print "Processing %d records from %s" % (len(records),
                        basename(filename))
            for record in records:
                to_db.save(record)
                if verbosity >= 2:
                    sys.stdout.write('.')
                    sys.stdout.flush()
