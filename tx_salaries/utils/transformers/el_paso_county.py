from datetime import date

from . import base
from . import mixins

from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'department': 'DEPARTMENT',
        'job_title': 'JOB TITLE',
        'hire_date': 'HIRE DATE',
        'status': 'PART FULL',
        'annual': 'ANNUAL RATE',
        'pay_rate': 'PAY RATE',
        'race': 'ETHNICITY',
        'gender': 'SEX'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'El Paso County'
    ORGANIZATION_CLASSIFICATION = 'County'

    DATE_PROVIDED = date(2013, 10, 31)
    # Y/M/D agency provided the data

    URL = "http://raw.texastribune.org.s3.amazonaws.com/path/to/rio_grande_county.xls"

    cleaver.DepartmentName.MAP = cleaver.DepartmentName.MAP + (
        (cleaver.regex_i(r'ADM\.$'), 'Administration'),
        (cleaver.regex_i(r'DIST ATTY'), 'District Attorney'),
        (cleaver.regex_i(r'COATTYADM'), 'County Attorney Administration'),
        (cleaver.regex_i(r'COATTY'), 'County Attorney'),
        (cleaver.regex_i(r'\-TAIP'), '- Treatment Alternative to Incarceration Program'),
        (cleaver.regex_i(r'AP COMMUNITY INTERVENTION CTR'), 'Adult Probation Community Intervention Center'),
        (cleaver.regex_i(r'ADULT PROB-GANG INTERVENTION'), 'Adult Probation - Gang Intervention'),
    )

    @property
    def is_valid(self):
        # Georgina Torres invalid hire date
        return self.last_name.strip() != '' and self.hire_date != '00/00/0000'

    @property
    def compensation_type(self):
        if self.status.upper() == 'F':
            return 'FT'
        else:
            return 'PT'

    @property
    def identifier(self):
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data, exclude=['PAY RATE', ]),
        }

    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('/'))
        try:
            hire_date = date(hire_date_data[2], hire_date_data[0],
                         hire_date_data[1])
        except:
            return None
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
            raise ValueError(error_msg)
        return tenure

    @property
    def compensation(self):
        if self.annual.strip() == '0':
            return self.pay_rate
        else:
            return self.annual

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]

transform = base.transform_factory(TransformedRecord)
