from datetime import date

from . import base
from . import mixins

from .. import cleaver

# http://raw.texastribune.org.s3.amazonaws.com/ut_el_paso/salaries/2014-02/Hill%2C%20Dan_TexasTribune_01-13-14.xlsx


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
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
        'race': 'ETHNICITY',
        'gender': 'GENDER',
        'compensation': 'FY ALLOCATIONS'
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', 'suffix_name')

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    ORGANIZATION_NAME = 'University of Texas at El Paso'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet, 40 earn < 4000
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 2, 25)

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r'Utep'), 'UTEP'), ) +
                                 ((cleaver.regex_i(r'^Ktep'), 'KTEP'), ) +
                                 ((cleaver.regex_i(r'^Mpa'), 'MPA'), ) +
                                 ((cleaver.regex_i(r' Pc '), 'PC'), ) +
                                 ((cleaver.regex_i(r' Hpc '), 'HPC'), ) +
                                 ((cleaver.regex_i(r'Mc/Pc'), 'MC/PC'), ))

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def process_full_name(self):
        # can't use get_raw_name because middle and suffix only sometimes given
        first = self.first_name.strip()
        last = self.last_name.strip()
        middle = self.middle_name.strip()
        suffix_name = self.suffix_name.strip()

        name = first
        if middle != "":
            name += " %s" % middle
        name += " %s" % last
        if suffix_name != "":
            name += " %s" % suffix_name
        return name

    @property
    def person(self):
        data = {
            'family_name': self.last_name.strip(),
            'given_name': self.first_name.strip(),
            'name': self.process_full_name()
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data

    def process_hire_date(self, hire_date):
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
                    'name': unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                           .parse()),
                },
            }
        ]

    @property
    def post(self):
        return {'label': (unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                         .parse()))}

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]

transform = base.transform_factory(TransformedRecord)
