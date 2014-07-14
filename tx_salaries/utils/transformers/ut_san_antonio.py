from datetime import date

from . import base
from . import mixins

from .. import cleaver

# http://raw.texastribune.org.s3.amazonaws.com/ut_san_antonio/salaries/2014-01/Hill1931-responsive.xls


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'department': 'Department',
        'job_title': 'Job Title',
        'hire_date': 'Hire Date',
        'race': 'Ethnicity',
        'gender': 'Sex',
        'compensation': 'Annual Salary',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'Female': 'F', 'Male': 'M'}

    ORGANIZATION_NAME = 'University of Texas at San Antonio'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO 45 earn < 10,000
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 1, 21)

    cleaver.DepartmentName.MAP = (cleaver.DepartmentName.MAP +
                                 ((cleaver.regex_i(r' Vc '), ' VC '), ) +
                                 ((cleaver.regex_i(r' Svcs '), ' SVCS '), ) +
                                 ((cleaver.regex_i(r' Svc'), ' SVC'), ) +
                                 ((cleaver.regex_i(r'Coe '), 'COE '), ) +
                                 ((cleaver.regex_i(r'Cob-Asc'), 'COB-ASC'), ) +
                                 ((cleaver.regex_i(r' Ofc '), ' OFC '), ) +
                                 ((cleaver.regex_i(r'Cos '), 'COS '), ) +
                                 ((cleaver.regex_i(r' Seri'), ' SERI'), ) +
                                 ((cleaver.regex_i(r'Ihdr'), 'IHDR'), ) +
                                 ((cleaver.regex_i(r'Mbc'), 'MBC'), ) +
                                 ((cleaver.regex_i(r'^Itc'), 'ITC'), ) +
                                 ((cleaver.regex_i(r'Swtaac'), 'SWTAAC'), ) +
                                 ((cleaver.regex_i(r'^Vp-'), 'VP-'), ) +
                                 ((cleaver.regex_i(r'^Tx'), 'TX'), ) +
                                 ((cleaver.regex_i(r'^Tv'), 'TV'), ) +
                                 ((cleaver.regex_i(r'^Rsc '), 'RSC '), ) +
                                 ((cleaver.regex_i(r'^Rsch '), 'RSCH '), ) +
                                 ((cleaver.regex_i(r' Rsrcs '), ' RSRCS '), ) +
                                 ((cleaver.regex_i(r'- Cob'), '- COB'), ))

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != '' and self.hire_date.strip() != ''

    def calculate_tenure(self):
        try:
            hire_date_data = map(int, self.hire_date.split('-'))
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
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure(),
                },
                'tx_salaries.EmployeeTitle': {
                    'name': unicode(cleaver.DepartmentNameCleaver(self.job_title)
                                           .parse())
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

    @property
    def person(self):
        data = {
            'family_name': self.last_name,
            'given_name': self.first_name,
            'name': self.get_raw_name(),
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data


transform = base.transform_factory(TransformedRecord)
