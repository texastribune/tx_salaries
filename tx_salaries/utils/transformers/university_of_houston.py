from . import base
from . import mixins

from datetime import date


class TransformedRecord(
        mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    REJECT_ALL_IF_INVALID_RECORD_EXISTS = False

    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Dept',
        'job_title': 'Job Title',
        'hire_date': 'Start Date',
        'compensation': 'Annual Rt',
        'employee_type': 'Full/Part',
        'gender': 'Sex',
        'nationality': 'Ethnic Grp',
        'campus': 'Unit',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    # The name of the organization this WILL SHOW UP ON THE SITE,
    # so double check it!
    # ORGANIZATION_NAME = 'University of Houston'

    # What type of organization is this?
    # This MUST match what we use on the site,
    # double check against salaries.texastribune.org
    ORGANIZATION_CLASSIFICATION = 'University'

    compensation_type = 'FT'

    description = 'Annual salary'

    campus_map = {
        'UH': 'University of Houston',
        'UH Clear Lake': 'University of Houston-Clear Lake',
        'UH Victoria': 'University of Houston-Victoria',
        'UH System': 'University of Houston System',
        'UH Downtown': 'University of Houston-Downtown',
    }

    # How do they track gender? We need to map what they use to `F` and `M`.
    gender_map = {'F': 'F', 'M': 'M'}

    DATE_PROVIDED = date(2016, 12, 1)
    # Y/M/D agency provided the data
    URL = ('https://s3.amazonaws.com/raw.texastribune.org/'
           'university_houston/salaries/2016-12/uh.xls')

    @property
    def organization(self):
        return {
            'name': self.campus_map[self.campus.strip()],
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        has_first_name = True if self.first_name else False
        has_last_name = True if self.last_name else False
        has_hire_date = True if self.hire_date else False
        has_salary = True if self.compensation else False

        return (
            has_first_name and has_last_name and has_hire_date and has_salary)

    @property
    def compensation_type(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return 'FT'

        if employee_type == 'P':
            return 'PT'

    @property
    def description(self):
        employee_type = self.employee_type

        if employee_type == 'F':
            return "Annual salary"

        if employee_type == 'P':
            return "Part-time annual salary"

    @property
    def race(self):
        race = self.nationality.strip()

        return {
            'name': race if race else ''
        }

transform = base.transform_factory(TransformedRecord)
