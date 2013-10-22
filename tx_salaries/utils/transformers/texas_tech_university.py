from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin,
        mixins.GenericJobTitleMixin,
        mixins.MembershipMixin,
        mixins.OrganizationMixin,
        mixins.PostMixin,
        base.BaseTransformedRecord):
    MAP = {
        'department': 'Department',
        'name': 'Name',
        'job_title': 'Title',
        'last_name': 'Last Name',
        'hire_date': 'Hire Date',
        'pay_status': 'FT or PT Status',
        'compensation': 'Salary',
        'race': 'Race',  # Not used yet
    }

    NAME_FIELDS = ('name', )
    ORGANIZATION_NAME = 'Texas Tech University'

    # The data we get for Texas Tech System is always valid
    is_valid = True

    # All employees are full-time right now
    compensation_type = 'Full Time'

    @property
    def identifier(self):
        """
        Identifier by Texas Tech Systems

        Ignore everything but name/gender.  We have not found any
        duplicate name gender records (yet), and should not as TT
        includes middle initials.
        """
        excluded = [self.race_key, self.department_key, self.job_title_key,
                self.hire_date_key, self.compensation_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=excluded)
        }

    @property
    def person(self):
        name = self.get_name()
        return {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }


def transform(labels, source):
    """
    Custom transform parser for Texas Tech Universities

    Texas Tech Systems provide spreadsheets with merge cells in them.
    This means that a row might not include all of the information
    required to build a record.
    """
    data = []
    counter = 0
    last_row = None
    for raw_row in source:
        counter += 1
        row = dict(zip(labels, raw_row))
        if not raw_row[0].strip() and last_row:
            for key, value in last_row.items():
                if not row[key]:
                    row[key] = last_row[key]

        record = TransformedRecord(row)
        data.append(record.as_dict())
        last_row = row
    return data
