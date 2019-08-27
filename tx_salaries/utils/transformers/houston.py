from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last name',
        'first_name': 'First name',
        'middle_name': 'Middle name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annual Salary',
        'gender': 'Gender',
        'race': 'Racial Category',
        'employment_type': 'Employee Grp',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Houston'

    ORGANIZATION_CLASSIFICATION = 'City'

    description = 'Annual salary'

    DATE_PROVIDED = date(2019, 7, 17)

    URL = "http://raw.texastribune.org.s3.amazonaws.com/houston/salaries/2019-07/COH_revised_2018_calendar_year_v2.xlsx"

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        return self.last_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    @property
    def compensation(self):
        status = self.get_mapped_value('employment_type')

        if status == 'Full Time':
            return self.get_mapped_value('compensation')
        else:
            return 0


    @property
    def compensation_type(self):
        status = self.get_mapped_value('employment_type')

        if status == 'Full Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        status = self.get_mapped_value('employment_type')

        if status == 'Full Time':
            return 'Annual salary'
        elif status == 'HFD Deferred Term':
            return 'Deferred term: paid hourly rate'
        elif status == 'Temporary':
            return 'Temporary: paid hourly rate'
        elif 'Part Time' in status:
            return 'Part-time: paid hourly rate'

    @property
    def race(self):
        given_race = self.get_mapped_value('race')

        if given_race == '':
            given_race = 'Unknown/Not Specified'

        return {'name': given_race}

transform = base.transform_factory(TransformedRecord)
