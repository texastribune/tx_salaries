from django.core.management.base import BaseCommand

from ...utils import transformer


class Command(BaseCommand):
    def handle(self, filename, *args, **kwargs):
        reader = transformer.convert_to_csv_reader(filename)
        labels = reader.next()
        transformer_key = transformer.generate_key(labels)

        if transformer_key in transformer.TRANSFORMERS.keys():
            print transformer_key + ' (exists)'
        else:
            print transformer_key
