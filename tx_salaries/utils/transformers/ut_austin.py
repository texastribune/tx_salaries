from datetime import date

from . import base
from . import mixins

from .. import cleaver

# http://raw.texastribune.org.s3.amazonaws.com/ut_austin/salaries/2014-02/TexasTribuneUTAustinSalaryData02-11-14.xlsx


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'NAME LAST',
        'first_name': 'NAME FIRST',
        'middle_name': 'NAME MIDDLE',
        'suffix_name': 'NAME SUFFIX',
        'department': 'DEPARTMENT TITLE',
        'job_title': 'JOB TITLE',
        'hire_date': 'CONTINUOUS EMPLOYMENT DATE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'FY ALLOCATIONS',
    }

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Austin'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given, 29 < 4000
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 2, 14)

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r'vp '), 'Vice President '), ) +
                                 ((cleaver.regex_i(r'^Its '), 'ITS '), ) +
                                 ((cleaver.regex_i(r'^Kut '), 'KUT '), ) +
                                 ((cleaver.regex_i(r'^Phr '), 'PHR '), ) +
                                 ((cleaver.regex_i(r'^Fs '), 'FS '), ) +
                                 ((cleaver.regex_i(r'^Dns '), 'DNS '), ) +
                                 ((cleaver.regex_i(r'^Pmcs '), 'PMCS '), ) +
                                 ((cleaver.regex_i(r'^Bfs '), 'BFS '), ) +
                                 ((cleaver.regex_i(r'Aces - It '), 'ACES - IT '), ) +
                                 ((cleaver.regex_i(r'Uteach'), 'UTeach'), ))

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def process_hire_date(self, hire_date):
        #19 cases
        if hire_date.strip() == "":
            return ""
        year = hire_date[0:4]
        month = hire_date[4:6]
        day = hire_date[6:8]
        return "-".join([year, month, day])

    @property
    def get_raw_name(self):
        # TODO include suffix
        if self.middle_name.strip() == '':
            self.NAME_FIELDS = ('first_name', 'last_name')
        name_fields = [getattr(self, a).strip() for a in self.NAME_FIELDS]
        return u' '.join(name_fields)

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
                },
                'tx_salaries.Employee': {
                    'hire_date': hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure(hire_date),
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
            }
        ]

    @property
    def post(self):
        return {'label': (unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                         .parse()))}

    @property
    def given_race(self):
        return {'name': self.race.strip()}

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]

transform = base.transform_factory(TransformedRecord)
