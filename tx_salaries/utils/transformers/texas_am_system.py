from . import base
from . import mixins

from datetime import date


class TransformedRecord(mixins.GenericCompensationMixin,
                        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
                        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
                        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
                        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LastName',
        'first_name': 'FirstName',
        'department': 'ShortAdlocDesc',
        'job_title': 'ShortTitleDesc',
        'hire_date': 'OrigEmplDate',
        'compensation': 'BudgetedSalary',
        'gender': 'Sex',
        'minority_code': 'EEOMinorityCode',
        'organization_name': 'MbrName',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_CLASSIFICATION = 'University'

    DATE_PROVIDED = date(2014, 1, 15)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/texas_a%26m_university_system/salaries/2014-01/Hill%20-%20SO-14-003.xlsx'

    compensation_type = 'FT'
    description = 'Annual compensation'

    race_map = {
        '': 'Not given',
        '1': 'White (Not Hispanic or Latino)',
        '2': 'Black or African American (Not Hsp/Lt)',
        '3': 'Hispanic or Latino',
        '4': 'Asian (Not Hispanic or Latino)',
        '5': 'Amer Indian or Alaskan Ntv (Not Hsp/Lt)',
        '6': 'Ntv Hawaiian/Oth Pcfc Isldr (Not Hsp/Lt)',
        '7': 'Two or More Races (Not Hispanic/Latino)',
    }

    @property
    def organization(self):
        return {
            'name': self.organization_name,
            'children': self.department_as_child,
            'classification': self.ORGANIZATION_CLASSIFICATION,
        }

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def race(self):
        return {
            'name': self.race_map[self.minority_code.strip()]
        }

transform = base.transform_factory(TransformedRecord)
