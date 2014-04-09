from . import base
from . import mixins

from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'LAST NAME',
        'first_name': 'FIRST NAME',
        'department': ' AGENCY NAME',
        'job_title': 'CLASS TITLE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'hire_date': 'HIRE DATE',
        'compensation': 'ANNUAL SALARY',
        'compensation_type': 'EMPLOYEE TYPE',
        'agency_number': 'AGENCY',
        'state_number': 'STATE NUMBER'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    gender_map = {'FEMALE': 'F', 'MALE': 'M'}

    ORGANIZATION_NAME = 'State of Texas'

    ORGANIZATION_CLASSIFICATION = 'State'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    def get_cleaved_first_or_last(self, name):
        return str(cleaver.EmployeeNameCleaver(name).parse())

    @property
    def person(self):
        data = {
            'family_name': self.get_cleaved_first_or_last(self.last_name.strip()),
            'given_name': self.get_cleaved_first_or_last(self.first_name.strip()),
            'name': self.get_name(),
        }
        try:
            data.update({
                'gender': self.gender_map[self.gender.strip()]
            })
            return data
        except KeyError:
            return data

    def process_compensation_type(self):
        # only grab "Full Time" or "Part Time" subsets
        return u' '.join(self.compensation_type.strip()[-9:].title().split('-'))


    @property
    def compensations(self):
        compensation_type = self.process_compensation_type()
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': compensation_type,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title.strip(),
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
