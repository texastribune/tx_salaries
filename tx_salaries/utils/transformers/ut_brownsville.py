from datetime import date

from . import base
from . import mixins

# http://raw.texastribune.org.s3.amazonaws.com/ut_brownsville/salaries/2014-01/PIR%20662.xlsx


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, base.BaseTransformedRecord):
    MAP = {
        'last_name': 'Last Name',
        'first_name': 'First Name',
        'middle_name': 'Middle Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Hire Date',
        'compensation': 'Annualized',
        'race': 'Race',
        'gender': 'Gender'
    }

    NAME_FIELDS = ('first_name', 'last_name', )

    ORGANIZATION_NAME = 'University of Texas at Brownsville'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet, but they appear to give part time
    compensation_type = 'Full Time'

    DATE_PROVIDED = date(2014, 1, 24)

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.last_name.strip() != ''

    @property
    def identifier(self):
        """
        Identifier for UT Brownsville
        """
        excluded = [self.department_key, self.job_title_key,
                    self.hire_date_key, self.compensation_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=excluded)
        }


transform = base.transform_factory(TransformedRecord)
