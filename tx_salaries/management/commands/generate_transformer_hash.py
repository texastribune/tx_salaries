from django.core.management.base import BaseCommand
from optparse import make_option

from ...utils import transformer


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sheet', action='store', dest='sheet', default=None,
                    help='Sheet name'),
        make_option('--row', action='store', dest='label_row', default=1,
                    help='Location of the row of labels, defaults to 1'),
    )

    def handle(self, filename, label_row=1, sheet=None, *args, **kwargs):
        reader = transformer.convert_to_csv_reader(filename, sheet=sheet)
        for i in range(1, int(label_row)):
            reader.next()
        labels = reader.next()
        print transformer.generate_key(labels)
