import re

from datetime import date

from . import base
from . import mixins

ARTICLES = ['a', 'an', 'the', ]
CONJUNCTIONS = ['and', 'but', 'for', 'nor', 'or', ]
PREPOSITIONS = ['at', 'by', 'for', 'in', 'of', 'on', 'to', ]
ABBREVIATIONS = ['hhs', 'hr', 'hvac', 'tdcj', 'vc', ]

STOP_WORDS = ARTICLES + CONJUNCTIONS + PREPOSITIONS

ROMAN_NUMERAL_REGEX = re.compile('^(X|IX|IV|V?I{0,3})$', re.I)
APOSTROPHE_LETTER_REGEX = re.compile("([a-z])'([A-Z])")
DIGIT_LETTER_REGEX = re.compile(r'\d([A-Z])')
COMMA_REGEX = re.compile(r',\s*')


def better_title(value):
    """Convert a string into titlecase."""
    t = APOSTROPHE_LETTER_REGEX.sub(
        lambda m: m.group(0).lower(), value.title())
    return DIGIT_LETTER_REGEX.sub(lambda m: m.group(0).lower(), t)


def normalize_organization_name(name):
    output = []

    for idx, s in enumerate(name.split()):
        word = s.lower()

        # if the word is a valid abbreviation, always uppercase it
        if word in ABBREVIATIONS:
            converted = word.upper()
        # if this is the first word, it should be capitalized
        elif idx == 0:
            converted = better_title(s)
        # if this is a valid stop word, it should remain lowercase
        elif word in STOP_WORDS:
            converted = word
        # if this is a Roman numeral, it should be uppercase
        elif ROMAN_NUMERAL_REGEX.match(word):
            converted = word.upper()
        # finally, just treat it normally otherwise
        else:
            converted = better_title(s)

        output.append(converted)

    combined_output = ' '.join(output)
    return ', '.join(COMMA_REGEX.split(combined_output))


class TransformedRecord(
    mixins.GenericCompensationMixin,
    mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
    mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
    mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):

    MAP = {
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'middle_name': 'MI',
        'department': 'AGENCY NAME',
        'job_title': 'CLASS TITLE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'hire_date': 'EMPLOY DATE ',
        'compensation': 'ANNUAL',
        'compensation_type': 'STATUS',
        'agency_number': 'AGENCY',
        'state_number': 'STATE NUMBER',
    }

    NAME_FIELDS = ('first_name', 'middle_name', 'last_name', )

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
    status_map = {
        'F': 'FT',
        'P': 'PT',
    }

    gender_map = {
        'FEMALE': 'F',
        'MALE': 'M',
    }

    ORGANIZATION_NAME = 'State Comptroller Payroll'

    ORGANIZATION_CLASSIFICATION = 'State'

    DATE_PROVIDED = date(2018, 4, 26)

    URL = ('https://s3.amazonaws.com/raw.texastribune.org/state_of_texas/'
           'salaries/2018-05/state_of_texas.csv')

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.first_name.strip() != ''

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender_map[self.gender.strip()]
        }

        return r

    def process_compensation_type(self):
        '''
        Use the last letter of the code to determine part time or full time
        '''
        compensation_type = self.compensation_type.split(' - ')[0]
        return self.status_map[compensation_type[-1]]

    def process_compensation_description(self):
        compensation_description = self.compensation_type.split(' - ')[1]
        return normalize_organization_name(compensation_description.strip())

    def process_job_title(self):
        return normalize_organization_name(self.data['CLASS TITLE'])

    @property
    def post(self):
        return {'label': self.process_job_title()}

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
        return [{
            'name': normalize_organization_name(self.department)
        }]


transform = base.transform_factory(TransformedRecord)
