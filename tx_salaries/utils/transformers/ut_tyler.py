from . import base
from . import mixins


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericDepartmentMixin, mixins.GenericIdentifierMixin,
        mixins.GenericJobTitleMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'full_name': 'NAME',
        'department': 'SHORT-DEPT',
        'job_title': 'JOB-TITLE',
        'gender': 'GENDER',
        'race': 'ETHNICITY',
        'hire_date': 'DATE-HIRED',
        'compensation': 'RATE',
        'full_time': 'PERCENT',
        'active': 'ACTIVE-GRP',
        'appt': 'APPT',
        'mo_hr': 'MO-HR',
        'emp_type': 'TYPE'
    }

    ORGANIZATION_NAME = 'The University of Texas at Tyler'

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    def process_name(self, name):
        split_name = name.split(',')
        return {
            'given_name': split_name[1].strip(),
            'family_name': split_name[0].strip()
        }

    @property
    def person(self):
        names = self.process_name(self.full_name)
        data = {
            'family_name': names['family_name'],
            'given_name': names['given_name'],
            'name': " ".join([names['family_name'], names['given_name']]),
            'gender': self.gender,
        }
        return data

    def process_compensation_type(self, full_time):
        """

        "If someone's percentage time says 10000 that is equivalent to 100% or Full-Time.
        You will see some people have more than one job/appointment but equal up to 100% time.
        Anyone under 10000 or 100% will be part-time"

        """
        if int(full_time.strip()) == 10000:
            return 'Full Time'
        else:
            return 'Part Time'

    @property
    def compensations(self):
        compensation_type = self.process_compensation_type(self.full_time)
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
                    'name': self.job_title,
                },
            }
        ]

    @property
    def identifier(self):
        """
        Identifier based only on name/gender/ethnicity.

        "People also may have more than one job in departments"
        """
        excluded = [self.full_time_key, self.department_key,
                    self.compensation_key,
                    self.hire_date_key, self.job_title_key,
                    self.race_key, self.gender_key,
                    self.active_key, self.emp_type_key,
                    self.mo_hr_key, self.appt_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=excluded)
        }

transform = base.transform_factory(TransformedRecord)
