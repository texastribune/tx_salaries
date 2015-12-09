from datetime import date

from . import base
from . import mixins
from decimal import Decimal


class TransformedRecord(mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
                        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
                        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
                        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First',
        'job_title': 'Job Title',
        'department': 'Dept Descr',
        'full_time': 'FTE',
        'compensation': 'Annual Rt',
        'gender': 'Gender',
        'hire_date': 'Hire Date',
        'race': 'Ethnicity',
        'pay_group': 'Pay Group'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'The University of Texas at Tyler'

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2015, 9, 16)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_tyler/salaries/2015-09/ut_tyler.xls'

    description = 'Annual compensation'


    # there will be exception raised elsewhere if not valid
    is_valid = True

    @property
    def compensation_type(self):
        return 'FT' if self.full_time >= 1 else 'PT'

    @property
    def description(self):
        return {'F9M': 'Faculty pay group being paid over 9 months',
                'M19': 'Monthly pay group for NRA (Non-resident Alien) employees',
                'MNF': 'Monthly pay group for non-exempt employees (those who are eligible for '
                       'overtime pay based on FLSA standards)',
                'MON': 'Monthly pay group for exempt employees (those who are not eligible for '
                       'overtime pay based on FLSA standards)',
                'S19': 'Semi-monthly pay group for NRA (Non-resident Alien) employees',
                'SMF': 'Semi-monthly pay group for non-exempt employees (those who are eligible for '
                       'overtime pay based on FLSA standards)',
                'SMN': 'Semi-monthly pay group for exempt employees (those who are not eligible for '
                       'overtime pay based on FLSA standards)'
                }[self.pay_group.strip()]

    @property
    def identifier(self):
        """
        Identifier based only on name/gender/ethnicity.

        "People also may have more than one job in departments"
        """
        excluded = [self.job_title_key, self.department_key,
                    self.full_time_key, self.compensation_key,
                    self.hire_date_key, self.pay_group_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                                                      exclude=excluded)
        }


# Since there is a lot of code assuming people can't hold multiple jobs, including aggregations and views,
# I am doing a very hacky thing. For each person with multiple jobs, we give them a job 'Multiple',
# go with thier least recent hire date, and give them the department description "multiple departments", and call it a day
def special_sauce_transform(labels, source, record_class):
    sorted_data = []

    for raw_record in source:
        sorted_data.append(raw_record)

    # problem inherent in the way they are giving us data that I can't code away:
    # if a person has the same last and first and gender and ethnicity as another person, it's impossible to
    # keep from grouping them together. Not enough info here'
    key_indices = [labels.index(k) for k in ['Last', 'First', 'Gender', 'Ethnicity']]

    def key_getter(row):
        return [row[index] for index in key_indices]

    sorted_data.sort(key=key_getter)

    def get_date(date_string):
        dt = map(int, date_string.split('-'))
        return date(*dt)

    # the wonderful and all wise CSVKit returns empty strings
    # for a number field if the number field is 0
    def get_decimal(string):
        return Decimal(string) if len(string.strip()) != 0 else Decimal()

    grouped_data = []
    label_index_mapping = {key: value for value, key in enumerate(labels)}
    previous_datum = sorted_data.pop(0)
    previous_datum[label_index_mapping['FTE']] = get_decimal(previous_datum[label_index_mapping['FTE']])
    previous_datum[label_index_mapping['Annual Rt']] = get_decimal(previous_datum[label_index_mapping['Annual Rt']])
    for datum in sorted_data:
        datum[label_index_mapping['FTE']] = get_decimal(datum[label_index_mapping['FTE']])
        datum[label_index_mapping['Annual Rt']] = get_decimal(datum[label_index_mapping['Annual Rt']])
        if key_getter(previous_datum) == key_getter(datum):
            previous_datum[label_index_mapping['Job Title']] = 'Multiple'
            previous_datum[label_index_mapping['Dept Descr']] = 'Multiple'
            previous_datum[label_index_mapping['FTE']] += datum[label_index_mapping['FTE']]
            previous_datum[label_index_mapping['Annual Rt']] += datum[label_index_mapping['Annual Rt']]

            if get_date(previous_datum[label_index_mapping['Hire Date']]) > \
                    get_date(datum[label_index_mapping['Hire Date']]):
                previous_datum[label_index_mapping['Hire Date']] = datum[label_index_mapping['Hire Date']]

        else:
            grouped_data.append(previous_datum)
            previous_datum = datum
    grouped_data.append(previous_datum)
    return base.generic_transform(labels, grouped_data, record_class)


transform = base.transform_factory(TransformedRecord, transform_func=special_sauce_transform)
