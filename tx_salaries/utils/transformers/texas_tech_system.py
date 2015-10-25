from . import base
from . import mixins
from datetime import date
from decimal import Decimal

GENDER_COLUMN_KEY = 'Gender'
RACE_COLUMN_KEY = 'Race'
class TransformedRecord(mixins.GenericCompensationMixin,
                        mixins.GenericDepartmentMixin,
                        mixins.GenericJobTitleMixin,
                        mixins.MembershipMixin,
                        mixins.OrganizationMixin,
                        mixins.PostMixin,
                        mixins.LinkMixin,
                        base.BaseTransformedRecord):
    MAP = {
        'department': 'Organization ',
        'name': 'Name ',
        'job_title': 'Position ',
        'hire_date': 'Current Hire Date',
        'pay_status': 'Employee Classification',
        'compensation': 'Salary',
        'race': RACE_COLUMN_KEY,
        'gender': GENDER_COLUMN_KEY,
    }

    NAME_FIELDS = ('name',)
    ORGANIZATION_NAME = 'Texas Tech University'

    URL = ('http:///www.google.com/')
    DATE_PROVIDED = date(2015, 10, 16)
    description = 'Annual Salary'

    @property
    def job_title(self):
        job_title = self.get_mapped_value('job_title')
        if type(job_title) == list:
            return '/'.join(sorted(list(set(job_title))))
        return job_title

    @property
    def compensation(self):
        compensation = self.get_mapped_value('compensation')
        if type(compensation) == list:
            return sum([Decimal(value) for value in compensation])
        assert type(compensation) == str or type(compensation) == unicode
        return compensation

    @property
    def compensation_type(self):
        pay_split = self.pay_status.split(' ')[0]
        # assert pay_split == 'FT' or pay_split == 'PT'
        if (pay_split == 'FT' and pay_split == 'PT'):
            return 'FT' # for now, till clarification, so I can debug code
        return pay_split

    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }

        gender = self.gender
        if gender.split() == '':
            gender = 'Not given'
        r['gender'] = gender

        return r

    @property
    def gender(self):
        gender = self.get_mapped_value('gender')
        if type(gender) == list:  # apparent clerical error, some people have multiple entries of same gender
            if len(set(gender)) == 1:
                return gender[0]
        assert type(gender) == str or type(gender) == unicode
        return gender

    @property
    def race(self):
        race = self.get_mapped_value('race')
        if type(race) == list:
            race.sort()  # sort it so any given combination of races will match between people in our race display
            race = '/'.join(race)
        assert type(race) == str or type(race) == unicode
        if len(race.strip()) == 0:
            race = 'Not available'
        return {
            'name': race
        }

    is_valid = True

    @property
    def organization_name(self):
        return self.ORGANIZATION_NAME

    @property
    def organization(self):
        return {
            'name': self.organization_name,
            'children': self.department_as_child,
        }

    @property
    def identifier(self):
        """
        Identifier by Texas Tech Systems

        Ignore everything but name/gender.  We have not found any
        duplicate name gender records (yet), and should not as TT
        includes middle initials.
        """
        excluded = [self.race_key, self.department_key, self.job_title_key,
                    self.hire_date_key, self.compensation_key, self.pay_status_key]
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                                                      exclude=excluded)
        }


transform = base.transform_factory(record_class=TransformedRecord,
                                   transform_func=base.generic_merge_cell_transform(
                                       keys_to_exclude_from_merge_detection=[GENDER_COLUMN_KEY, RACE_COLUMN_KEY])
                                   )
