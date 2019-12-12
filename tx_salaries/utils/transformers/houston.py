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
        # We received several sheets from Houston, one that had an important Status column
        # But was missing thousands of salaries
        # We have another one that has all the right salaries
        # But was missing the Status column
        # So we merged those two files into one
        # Which is why the compensation col needs to be 'Annual Salary_x'
        # The 'x' was added when the join happened
        # 'x' = the first sheet we joined on
        # 'y' = the second sheet we joined on
        'compensation': 'Annual Salary_x',
        'gender': 'Gender',
        'race': 'Racial Category',
        'employment_type': 'Employee Grp',
        'employment_subtype': 'Employee Subgroup',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Houston'

    ORGANIZATION_CLASSIFICATION = 'City'

    description = 'Annual salary'

    DATE_PROVIDED = date(2019, 7, 17)

    URL = "http://raw.texastribune.org.s3.amazonaws.com/houston/salaries/2019-11/TPIA_request_tt_edit.csv"

    gender_map = {'Female': 'F', 'Male': 'M'}

    @property
    def is_valid(self):
        # We have two people with names of 'NA'
        # So let's account for them
        if self.first_name == '' and self.last_name == 'YAO':
            self.first_name = 'NA'

        if self.last_name == '' and self.first_name == 'JOHN':
             self.last_name = 'NA'

        return self.first_name != ''

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
        compensation = self.get_mapped_value('compensation')

        if status == 'Full Time':
            return self.get_mapped_value('compensation')
        else:
            return 0


    @property
    def compensation_type(self):
        status = self.get_mapped_value('employment_type')
        compensation = self.get_mapped_value('compensation')

        if status == 'Full Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def department(self):
        dept = self.get_mapped_value('department').replace("'S","'s")

        return dept

    @property
    def description(self):
        status = self.get_mapped_value('employment_type')
        sub_status = self.get_mapped_value('employment_subtype')

        if status == 'Full Time':
            return 'Annual salary'
        elif status == 'HFD Deferred Term':
            return 'Deferred term: Paid hourly rate, which is not shown'
        elif status == 'Temporary':
            return 'Temporary: Paid hourly rate, which is not shown'
        elif 'Part Time' in status:
            return 'Part-time: Paid hourly rate, which is not shown'

    @property
    def race(self):
        given_race = self.get_mapped_value('race')

        if given_race == '':
            given_race = 'Unknown/Not Specified'

        return {'name': given_race}

transform = base.transform_factory(TransformedRecord)
