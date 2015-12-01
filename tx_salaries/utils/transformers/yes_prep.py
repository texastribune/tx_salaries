from datetime import date

from . import mixins
from . import base


class TransformedRecord(mixins.GenericCompensationMixin, mixins.GenericDepartmentMixin,
                        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
                        mixins.GenericJobTitleMixin,
                        mixins.MembershipMixin, mixins.OrganizationMixin,
                        mixins.PostMixin, mixins.LinkMixin,
                        mixins.CompensationMap, base.BaseTransformedRecord):
    RACE_MAP = {
        'is_american_indian': 'American Indian or Alaska Native',
        'is_asian': 'Asian',
        'is_african_american': 'Black or African American',
        'is_pacific_islander': 'Native Hawaiian/Other Pacific Islander',
        'is_white': 'White',
    }

    MAP = {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'job_title': 'Job Title',
        'department': 'Department',
        'gender': 'Gender',
        'hire_date': 'Hire Date',
        'compensation': 'Salary/Hourly Rate',
        'compensation_type': 'Employment Status',
        'is_hispanic': 'Ethnicity',
    }

    MAP.update(RACE_MAP)

    COMPENSATION_MAP = {
        'Full Time': 'FT',
        'Part Time': 'PT',
    }

    NAME_FIELDS = ('first_name', 'last_name')

    ORGANIZATION_NAME = 'YES Prep Public Schools'

    ORGANIZATION_CLASSIFICATION = 'School District'  # Different from school district?

    DATE_PROVIDED = date(2015, 11, 20)

    is_valid = True

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/yes_prep/2015-11/2015-11-20.xlsx'

    @property
    def race(self):
        race_labels = []
        for key in self.RACE_MAP:
            if getattr(self, key).strip().upper() == 'X':
                race_labels.append(self.RACE_MAP[key])
        if self.is_hispanic.strip().upper() == 'HISP':
            # This is imperfect. They might only consider themselves hispanic but it appears
            # they have to have provided at least one race among the races in RACE_MAP
            race_labels.append('Hispanic')

        race_labels.sort()
        return {'name': ' and '.join(race_labels) if len(race_labels) > 0 else 'Not given'}

    @property
    def description(self):
        return self.get_mapped_value('compensation_type')


transform = base.transform_factory(TransformedRecord)
