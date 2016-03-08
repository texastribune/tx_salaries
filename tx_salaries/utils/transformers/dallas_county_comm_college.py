from datetime import date

from . import base
from . import mixins


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'Last Name ',
        'first_name': 'First Name ',
        'middle_name': 'Middle Name ',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Latest Hire Date',
        'gender': 'Gender',
        'given_race': 'Ethnicity/Race',
        'employee_type': 'Emp Type',
        'compensation': 'Annual Salary',
        'rate': 'Hrly Rate',
    }

    gender_map = {u'Female': u'F', u'Male': u'M'}

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'Dallas County Community College District'

    ORGANIZATION_CLASSIFICATION = 'Community College'

    DATE_PROVIDED = date(2016, 2, 17)

    URL = ('http://s3.amazonaws.com/raw.texastribune.org/dallas_county_'
           'community_college_district/salaries/2016-02/dcccd.xlsx')

    # There are some adjuncts who don't have a salary or wage
    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    @property
    def is_valid(self):
        return self.job_title.strip() != 'Pt Faculty, Non-Credit'

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
