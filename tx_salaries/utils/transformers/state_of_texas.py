import re

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
        'department': 'AGENCY NAME',
        'job_title': 'CLASS TITLE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'hire_date': 'HIRE DATE',
        'compensation': 'ANNUAL SALARY',
        'compensation_type': 'EMPLOYEE TYPE',
        'agency_number': 'AGENCY',
        'state_number': 'STATE NUMBER',
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    # State of Texas uses these employment status codes:
    description_map = {
        'URP': 'UNCLASSIFIED REGULAR PART-TIME',
        'URF': 'UNCLASSIFIED REGULAR FULL-TIME',
        'UTP': 'UNCLASSIFIED TEMPORARY PART-TIME',
        'UTF': 'UNCLASSIFIED TEMPORARY FULL-TIME',
        'ERF': 'EXEMPT REGULAR FULL-TIME',
        'CRF': 'CLASSIFIED REGULAR FULL-TIME',
        'CRP': 'CLASSIFIED REGULAR PART-TIME',
        'CTF': 'CLASSIFIED TEMPORARY FULL-TIME',
        'CTP': 'CLASSIFIED TEMPORARY PART-TIME',
    }
    status_map = {'F': 'FT', 'P': 'PT'}

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    ORGANIZATION_NAME = 'State Comptroller Payroll'

    ORGANIZATION_CLASSIFICATION = 'State'

    DATE_PROVIDED = date(2016, 2, 29)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/state_of_texas/salaries/2016-02/USPS_SPRS_ASOFJAN312016_.xlsx'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    def process_compensation_type(self):
        '''
        Use the last letter of the code to determine part time or full time
        '''
        return self.status_map[self.compensation_type.strip()[-1]]

    def process_compensation_description(self):
        return self.description_map[self.compensation_type.strip()].title()

    def process_job_title(self):
        # don't titlecase roman numerals
        roman_regex = re.compile("^(IX|IV|V?I{0,3})")

        def is_roman(snippet):
            if len(roman_regex.match(snippet).group()) > 0:
                return snippet
            else:
                return snippet.title()

        return (u" ").join([is_roman(s) for s in self.data["CLASS TITLE"]
                                                     .split(" ")])

    @property
    def post(self):
        return {'label': self.process_job_title()}

    # @property
    # def hire_date(self):
    #     raw_date = self.get_mapped_value('hire_date')
    #     print raw_date
    #     print '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])
    #     return '-'.join([raw_date[-4:], raw_date[:2], raw_date[3:5]])

    def calculate_tenure(self):
        # hire_date = self.get_mapped_value('hire_date')
        hire_date_data = map(int, self.hire_date.split('-'))
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
        compensation_type = self.process_compensation_type()
        description = self.process_compensation_description()
        job_title = self.process_job_title()
        tenure = self.calculate_tenure()
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': compensation_type,
                    'description': description,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                    'tenure': tenure,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': job_title,
                },
            }
        ]

    @property
    def identifier(self):
        """
        Identifier for State of Texas

        Includes STATE NUMBER
        """
        excluded = [self.department_key, self.job_title_key,
                    self.hire_date_key, self.compensation_key,
                    self.compensation_type_key, self.agency_number_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                                                      exclude=excluded)
        }

    @property
    # department names have trailing whitespace
    def department_as_child(self):
        if self.department == "Governor'S Office, Trustee Programs":
            # TODO make dept name cleaver handle this case
            return [{'name': "Governor's Office, Trustee Programs", }, ]
        return [{'name': unicode(cleaver.DepartmentNameCleaver(self.department)
                                        .parse()), }, ]


transform = base.transform_factory(TransformedRecord)
