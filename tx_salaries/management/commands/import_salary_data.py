import sys

from django.core.management.base import BaseCommand
from optparse import make_option
from os.path import basename

from ...utils import to_db, transformer
from ... import models


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
            if verbosity >= 2:
                print "Processing %d records from %s" % (len(records),
                        basename(filename))

            records_remaining = len(records)

            try:
                parent_org = self.get_parent_org(records[0])
            except:
                parent_org = None

            if parent_org:
                parent_org_employees = (models.Employee.objects
                               .filter(position__organization__parent=parent_org))
                while parent_org_employees.count():
                    # delete employees in batches of 100
                    employee_ids = parent_org_employees.values_list('pk', flat=True)[:100]
                    parent_org_employees.filter(pk__in=employee_ids).delete()
                parent_org_children = (models.Organization.objects
                                .filter(parent=parent_org))
                while parent_org_children.count():
                    # delete organizations in batches of 100
                    children_ids = parent_org_children.values_list('pk', flat=True)[:10]
                    parent_org_children.filter(pk__in=children_ids).delete()

            for record in records:
                to_db.save(record)
                records_remaining -= 1
                if verbosity == 1:
                    out('.')
                elif verbosity == 2 and records_remaining % 100 == 0:
                    print "%s records remaining" % records_remaining
                elif verbosity >= 3 and records_remaining % 500 == 0:
                    print "%s records remaining" % records_remaining

            if verbosity == 1:
                out('\n')

    def get_parent_org(self, first_record):
        parent_org_name = first_record['tx_people.Organization']['name']
        return models.Organization.objects.get(name=parent_org_name)
