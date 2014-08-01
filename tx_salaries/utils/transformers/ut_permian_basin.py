from datetime import date

from . import base
from . import mixins

from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'middle_name': 'NAME MIDDLE',
        'suffix_name': 'NAME SUFFIX',
        'department': 'DEPARTMENT TITLE',
        'job_title': 'JOB TITLE',
        'hire_date': 'CONTINUOUS EMPLOYMENT DATE',
        'status': 'LABEL FOR FT/PT STATUS',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'compensation': 'FY ALLOCATIONS',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    ORGANIZATION_NAME = 'University of Texas of the Permian Basin'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO 14 people earn < 4000
    compensation_type = 'FT'
    description = 'Annual compensation'

    DATE_PROVIDED = date(2014, 2, 14)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_permian_basin/salaries/2014-02/UTPB%20Request%20%2314050102~TexasTribuneUTPermianBasinSalaryData02-11-14.xlsx'

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r' Vc '), ' VC '), ))

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
        return self.last_name.strip() != '' and self.hire_date.strip() != ''

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

    @property
    def given_race(self):
        return {'name': self.race.strip()}

    def process_hire_date(self, hire_date):
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    def calculate_tenure(self, hire_date):
        try:
            hire_date_data = map(int, hire_date.split('-'))
        except:
            return None
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
            raise ValueError(error_msg)
        return tenure

    @property
    def compensations(self):
        hire_date = self.process_hire_date(self.hire_date)
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description
                },
                'tx_salaries.Employee': {
                    'hire_date': hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure(hire_date)
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]


transform = base.transform_factory(TransformedRecord)
