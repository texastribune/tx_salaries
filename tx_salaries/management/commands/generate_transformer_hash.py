from django.core.management.base import BaseCommand

from ...utils import transformer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('filename')

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

    def handle(self, *args, **options):
        if options['sheet']:
            sheet = options['sheet']
        else:
            sheet = None

        if options['label_row']:
            label_row = options['label_row']
        else:
            label_row = 1

        filename = options['filename']

        reader = transformer.convert_to_csv_reader(filename, sheet=sheet)
        for i in range(1, int(label_row)):
            reader.next()
        labels = reader.next()
        transformer_key = transformer.generate_key(labels)

        if transformer_key in transformer.TRANSFORMERS.keys():
            print transformer_key + ' (exists)'
        else:
            print transformer_key
