from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'middle_name': 'NAME MIDDLE',
        'name_suffix': 'NAME SUFFIX',
        'department': 'DEPARTMENT TITLE',
        'job_title': 'JOB TITLE',
        'race': 'ETHNICITY',
        'gender': 'GENDER',
        'hire_date': 'CONTINUOUS EMPLOYMENT DATE',
        'compensation': 'FY ALLOCATIONS',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    ORGANIZATION_NAME = 'University of Texas at Arlington'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet, but they appear to give part time. 14 people earn < 4000
    compensation_type = 'Full Time'

    @property
    def get_raw_name(self):
        # TODO include suffix
        if self.middle_name.strip() == '':
            self.NAME_FIELDS = ('first_name', 'last_name')
        name_fields = [getattr(self, a).strip() for a in self.NAME_FIELDS]
        return u' '.join(name_fields)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def person(self):
        data = {
            'family_name': self.last_name.strip(),
            'given_name': self.first_name.strip(),
            'name': self.get_raw_name,
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data

    def process_hire_date(self, hire_date):
        # TODO five people don't have hire dates given
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    @property
    def compensations(self):
        hire_date = self.process_hire_date(self.hire_date)
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': hire_date,
                    'compensation': self.compensation,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

    @property
    def given_race(self):
        return {'name': self.race.strip()}

transform = base.transform_factory(TransformedRecord)
