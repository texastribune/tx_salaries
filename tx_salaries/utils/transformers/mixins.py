from . import base

from datetime import date


def title_case_property(key):
    """
    Simple property for title casing a mapped value

    TODO remove this? It makes a broad assumption that organization names and
    job titles can be title cased when there are many edge cases.
    """
    return property(lambda self: self.get_mapped_value(key).title())


class GenericCompensationMixin(object):
    """
    Adds a generic ``compensations`` property

    This expects a single compensation to be present and requires the
    following properties be available:

    * ``compensation_type``
    # ``description``
    * ``hire_date``
    * ``compensation``
    * ``DATE_PROVIDED``

    Expects hire_date to be given as YYYY-MM-DD format.
    Override hire_date with @property if that is not the case.
    """
    EMPLOYEES_HIRED_AFTER_SUBMISSION = False
    def calculate_tenure(self):
        hire_date_data = map(int, self.hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((self.DATE_PROVIDED - hire_date).days) / float(360)
        if tenure < 0:
            if not self.EMPLOYEES_HIRED_AFTER_SUBMISSION:
                error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
                raise ValueError(error_msg)

        return tenure if tenure >= 0 else 0  # prevent us from putting a negative number
                                             # into our tenure aggregation

    @property
    def compensations(self):
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                    'description': self.description
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
                    'tenure': self.calculate_tenure()
                },
            }
        ]


class GenericDepartmentMixin(object):
    """
    Adds a generic ``department`` property that is title cased

    This requires a ``department`` property to be specified as a mapped
    value.
    """
    department = title_case_property('department')


class GenericJobTitleMixin(object):
    """
    Adds a generic ``job_title`` property that is title cased

    This requires a ``job_title`` property to be specified as a mapped
    value.
    """
    job_title = title_case_property('job_title')


class GenericIdentifierMixin(object):
    """
    Adds a generic ``identifier`` property to the class

    Requires a ``compensation`` value to be set if using the
    ``BaseTransformedRecord``, otherwise it requires a
    ``compensation_key`` property.
    """
    @property
    def identifier(self):
        return {
            'scheme': 'tx_salaries_hash',
            'identifier': base.create_hash_for_record(self.data,
                    exclude=[self.compensation_key, ])
        }


class GenericPersonMixin(object):
    """
    Adds a generic ``person`` property that assumes only a simple name

    Note, this will add ``gender`` if that is a mapped value.
    """
    @property
    def person(self):
        name = self.get_name()
        r = {
            'family_name': name.last,
            'given_name': name.first,
            'additional_name': name.middle,
            'name': unicode(name),
        }

        if self.is_mapped_value('gender'):
            gender = self.get_mapped_value('gender')
            if gender.split() == '':
                gender = 'Not given'
            r['gender'] = gender

        return r


class RaceMixin(object):
    """
    Adds a generic ``race`` property that assumes only a simple race name

    Requires a ``race`` property to be available.
    """
    TWO_OR_MORE_RACE_STRING = 'Two or More Races'

    @property
    def race(self):
        race = self.get_mapped_value('race')

        # race is a marge cell and
        # therefore we should return "Two or More Races"
        if type(race) == list:
            race = self.TWO_OR_MORE_RACE_STRING
        else:
            race = race.strip()
            if race == '':
                race = 'Not given'
        return {
            'name': race
        }


class MembershipMixin(object):
    """
    Adds a generic ``membership`` property to the class

    Requires a ``hire_date`` property to be available.
    """
    @property
    def membership(self):
        return {
            'start_date': self.hire_date,
        }


class OrganizationMixin(object):
    """
    Adds a generic ``organization`` property to the class

    This requires that the class mixing it in adds ``ORGANIZATION_NAME``
    and ``ORGANIZATION_CLASSIFICATION`` properties of the main level agency or
    department and needs a``department`` property.
    """
    @property
    def organization(self):
        return {
            'name': self.ORGANIZATION_NAME,
            'classification': self.ORGANIZATION_CLASSIFICATION,
            'children': self.department_as_child,
        }

    @property
    def department_as_child(self):
        return [{'name': unicode(self.department), }, ]


class PostMixin(object):
    """
    Adds a generic ``post`` property to the class

    This requires that there is a ``job_title`` property be available
    on the class above.
    """
    @property
    def post(self):
        return {
            'label': self.job_title,
        }


class LinkMixin(object):
    """
    Adds a ``link`` property to an organization's raw salary information

    Requires a ``URL`` property to be available.
    """
    @property
    def links(self):
        return {
            'url': self.URL,
            'note': 'Salary information'
        }
