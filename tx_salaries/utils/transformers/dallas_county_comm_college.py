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
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'TITLE',
        'hire_date': 'Latest Hire Date',
        'gender': 'Gender',
        'given_race': 'Race/Ethnicity',
        'employee_type': 'Employee Type',
        'compensation': 'Annual Salary',
        'rate': 'Hourly Rate',
    }

    gender_map = {'Female': 'F', 'Male': 'M'}

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'Dallas County Community College District'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2017, 11, 20)

    URL = ('http://raw.texastribune.org.s3.amazonaws.com/dallas_county_community_college_district'
           '/salaries/2017-11/OpenRecordsRequest_TexasTribune.xlsx')

    # There are some adjuncts who don't have a salary or wage
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    @property
    def is_valid(self):
        return self.job_title.strip() != 'Faculty, Adjunct, Non-Credit'

    @property
    def compensation(self):
        salary = self.get_mapped_value('compensation')
        wage = self.get_mapped_value('rate')

        if salary == '0':
            return wage
        else:
            return salary

    @property
    def gender(self):
        sex = self.gender_map[self.get_mapped_value('gender')]
        if sex.strip() == "":
            return ""
        return sex.strip()

    @property
    def compensation_type(self):
        employee_type = self.employee_type.strip()

        if employee_type == 'Full-Time':
            return 'FT'
        else:
            return 'PT'

    @property
    def description(self):
        salaried = self.get_mapped_value('compensation')

        if salaried == '0':
            return "Hourly rate"
        else:
            return "Annual Salary"

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.get_mapped_value('gender')],
        }

        return r

    @property
    def race(self):
        race = self.given_race.strip()
        if race == '':
            race = 'Unknown'
        return {'name': race}

transform = base.transform_factory(TransformedRecord)
