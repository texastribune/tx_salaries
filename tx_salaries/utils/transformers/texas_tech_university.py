from datetime import date

from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin,
        mixins.GenericJobTitleMixin,
        mixins.MembershipMixin,
        mixins.OrganizationMixin,
        mixins.PostMixin,
        mixins.RaceMixin,
        mixins.LinkMixin,
        base.BaseTransformedRecord):
    MAP = {
        'department': 'Department',
        'name': 'Name',
        'job_title': 'Title',
        'last_name': 'Last Name',
        'hire_date': 'Original Hire Date',
        'compensation': 'Annual Salary',
        'race': 'Race',
        'gender': 'Gender',
    }

    compensation_type = 'FT'

    gender_map = {'Female': 'F', 'Femail': 'F', 'Male': 'M'}

    NAME_FIELDS = ('name', )
    ORGANIZATION_NAME = 'Texas Tech University'
    ORGANIZATION_CLASSIFICATION = 'University'

    # The data we get for Texas Tech System is always valid
    is_valid = True

    # All employees are full-time right now
    compensation_type = 'Full Time'
    description = 'This is not a real description'

    DATE_PROVIDED = date(2015, 4, 8)
    EMPLOYEES_HIRED_AFTER_SUBMISSION = True

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/texas_tech_university/salaries/2013-07/Faculty%20Open%20Records%20-%20Tribune.xlsx'

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
            'gender': self.gender_map[self.gender]
        }


transform = base.transform_factory(record_class=TransformedRecord,
        transform_func=base.generic_merge_cell_transform)
