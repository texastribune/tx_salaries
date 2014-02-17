from django.core.management.base import BaseCommand
from optparse import make_option

from ...utils import transformer


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sheet', action='store', dest='sheet', default=None,
                    help='Sheet name'),
        make_option('--file', action='store', dest='filename', default=None,
                    help='File location'),
    )

    def handle(self, filename=None, sheet=None, *args, **kwargs):
        if filename is None:
            sys.stderr.write('Must provide at least one file to process')
            return

        reader = transformer.convert_to_csv_reader(filename, sheet=sheet)
        labels = reader.next()
        print transformer.generate_key(labels)
