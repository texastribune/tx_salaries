# http://raw.texastribune.org.s3.amazonaws.com/potter_county/salaries/2014-06/Response%20to%20Request_Spreadsheet.xlsx
# exported xlsx to csv because in2csv failed

from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
    base.BaseTransformedRecord):
    MAP = {
        'full_name': 'Employee Name',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'gender': 'Gender',
        'given_race': 'DESCRIPT',
        'compensation': 'Annual Salary',
    }

    ORGANIZATION_NAME = 'Potter County'
    ORGANIZATION_CLASSIFICATION = 'County'

    DATE_PROVIDED = date(2014, 06, 17)
    # Y/M/D agency provided the data

    compensation_type = 'Full Time'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def department(self):
        return ''

    @property
    def race(self):
        r = self.given_race.split(' ')[:-1]
        return {'name': " ".join([n.title() for n in r])}

    @property
    def compensation(self):
        raw = self.get_mapped_value('compensation')
        # import ipdb; ipdb.set_trace();
        return raw.strip('$').replace(',', '')

    @property
    def person(self):
        formatted_name = self.get_name()
        data = {
            'family_name': formatted_name['last_name'].title(),
            'given_name': formatted_name['first_name'].title(),
            'name': " ".join([n.title() for n in formatted_name.values()])
        }
        return data

    def get_name(self):
        split_name = self.full_name.split(', ')
        last_name = split_name[0]
        split_firstname = split_name[1].split(' ')
        first_name = split_firstname[0]
        if len(split_firstname) == 2 and len(split_firstname[1]) == 1:
            middle_init = split_firstname[1]
        else:
            first_name = split_name[1]
            middle_init = ''
        return {
            'first_name': first_name,
            'middle_init': middle_init,
            'last_name': last_name
        }

transform = base.transform_factory(TransformedRecord)
