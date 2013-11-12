from django.core.management.base import BaseCommand

from ...utils import transformer


class Command(BaseCommand):
    def handle(self, filename, *args, **kwargs):
        reader = transformer.convert_to_csv_reader(filename)
        labels = reader.next()
        print transformer.generate_key(labels)
