from datetime import date

from . import base
from . import mixins

from .. import cleaver


class TransformedRecord(mixins.GenericCompensationMixin,
        mixins.GenericIdentifierMixin, mixins.GenericPersonMixin,
        mixins.MembershipMixin, mixins.OrganizationMixin, mixins.PostMixin,
        mixins.RaceMixin, mixins.LinkMixin, base.BaseTransformedRecord):
    MAP = {
        'full_name': 'Name',
        'department': 'Department',
        'job_title': 'Title',
        'hire_date': 'Start Date',
        'race': 'Race',
        'gender': 'Sex',
        'compensation': 'Annual Rt',
        'compensation_type': 'Full/Part'
    }

    COMPENSATION_MAP = {
        'F': 'FT',
        'P': 'PT'
    }

    ORGANIZATION_NAME = 'University of Texas at El Paso'

    ORGANIZATION_CLASSIFICATION = 'University'

    # TODO not given on spreadsheet, 40 earn < 4000
    compensation_type = 'FT'
    description = 'Annual compensation'

    DATE_PROVIDED = date(2016, 6, 21)

    URL = 'http://raw.texastribune.org.s3.amazonaws.com/ut_el_paso/salaries/2016-06/utep.xlsx'

    @property
    def person(self):
        name = self.get_name()

        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
            'gender': self.gender.strip()
        }

        return r

    @property
    def is_valid(self):
        # Adjust to return False on invalid fields.  For example:
        return self.full_name.strip() != ''

    @property
    def compensation_type(self):
        return self.COMPENSATION_MAP[self.get_mapped_value('compensation_type')]

    # def calculate_tenure(self, hire_date):
    #     try:
    #         hire_date_data = map(int, hire_date.split('-'))
    #     except:
    #         return None
    #     hire_date = date(hire_date_data[0], hire_date_data[1],
    #                      hire_date_data[2])
    #     tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
    #     if tenure < 0:
    #         error_msg = ("An employee was hired after the data was provided.\n"
    #                      "Is DATE_PROVIDED correct?")
    #         raise ValueError(error_msg)
    #     return tenure

    def get_name(self):
        return cleaver.EmployeeNameCleaver(
            self.get_mapped_value('full_name')).parse()

transform = base.transform_factory(TransformedRecord)
