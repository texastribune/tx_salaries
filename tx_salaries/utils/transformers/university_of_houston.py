from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
        mixins.GenericIdentifierMixin, mixins.GenericJobTitleMixin,
        mixins.GenericPersonMixin, mixins.MembershipMixin,
        mixins.OrganizationMixin, mixins.PostMixin, mixins.RaceMixin,
        mixins.LinkMixin, base.BaseTransformedRecord):

    # REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'full_name': 'Name',
        'department': 'Department Desc',
        'job_title': 'Job Title',
        'hire_date': 'Orig Hire Date',
        'compensation': 'Annual Rt',
        'employee_type': 'Full/Part',
        'gender': 'Sex',
        'nationality': 'Ethnic Grp',
        'campus': 'Campus'
    }

    NAME_FIELDS = ('full_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    # ORGANIZATION_NAME = 'University of Houston'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    # How do they track gender? We need to map what they use to `F` and `M`.
    # gender_map = {'F': 'F', 'M': 'M'}

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'university_houston/salaries/2019-03/campuses.xlsx')

    race_map = {
        'AMIND': 'American Indian',
        'ASIAN': 'Asian',
        'BLACK': 'Black',
        'HISPA': 'Hispanic',
        'NSPEC': 'Not Specified',
        'WHITE': 'White',
        'PACIF': 'Pacific Islander',
        'NHISP': 'Not Hispanic',
        '': 'Not Specified'
    }

    campus_map = {
        'HR730': 'University of Houston',
        'HR759': 'University of Houston-Clear Lake',
        'HR765': 'University of Houston-Victoria',
        'HR783': 'University of Houston System',
        'HR784': 'University of Houston-Downtown',
    }

    DATE_PROVIDED = date(2019, 3, 2)
    # Y/M/D agency provided the data

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def organization(self):
        r = {
            'name': self.campus_map[self.campus.strip()],
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

        return r

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return "Annual salary"

        if employee_type == 'P':
            return "Part-time annual salary"

    @property
    def race(self):
        return {
            'name': self.race_map[self.nationality.strip()]
        }

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def department(self):
        dept = self.get_mapped_value('department')

        return dept

    @property
    def job_title(self):
        job = self.get_mapped_value('job_title')

        return job


transform = base.transform_factory(TransformedRecord)
