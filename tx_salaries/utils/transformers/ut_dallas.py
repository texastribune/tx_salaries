from datetime import date

from . import base
from . import mixins

from .. import cleaver

# http://raw.texastribune.org.s3.amazonaws.com/ut_dallas/salaries/2014-02/FOIA%20Request%20-%20Tribune.xlsx

class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Job Description',
        'hire_date': 'Start Date',
        'race': 'Ethnic Group',
        'gender': 'Sex',
        'status': 'LABEL FOR FT/PT STATUS',
        'compensation': 'Annual Rate if Applicable',
        'hourly': 'Hourly Rate if Applicable',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Dallas'

    ORGANIZATION_CLASSIFICATION = 'University'

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_dallas/salaries/2014-02/FOIA%20Request%20-%20Tribune.xlsx'

    DATE_PROVIDED = date(2014, 2, 19)

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r'Cbh '), 'CBH '), ) +
                                 ((cleaver.regex_i(r'Ir  - Ais'), 'IR - AIS '), ) +
                                 ((cleaver.regex_i(r'Ir - Eas'), 'IR - EAS'), ) +
                                 ((cleaver.regex_i(r'Ipe-Pppe'), 'IPE-PPE'), ) +
                                 ((cleaver.regex_i(r'Atec'), 'ATEC'), ) +
                                 ((cleaver.regex_i(r'^Ecs'), 'ECS'), ) +
                                 ((cleaver.regex_i(r'^Nsm'), 'NSM'), ) +
                                 ((cleaver.regex_i(r'\s{2,}'), ' '), ))

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def compensation_type(self):
        if self.compensation.strip() != '':
            return 'FT'
        else:
            # TODO need hours worked
            return 'Hourly'

    @property
    def description(self):
        if self.compensation.strip() != '':
            return 'Annual compensation'
        else:
            return 'Hourly compensation'

    @property
    def compensations(self):
        tenure = self.calculate_tenure()
        comp = self.compensation if self.compensation.strip() != '' else self.hourly
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': comp,
                    'tenure': tenure,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                    .parse()),
                },
            }
        ]

    @property
    def department_as_child(self):
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]


transform = base.transform_factory(TransformedRecord)
