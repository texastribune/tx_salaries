from . import base


def title_case_property(key):
    """Simple property for title casing a mapped value"""
    return property(lambda self: self.get_mapped_value(key).title())


class GenericCompensationMixin(object):
    """
    Adds a generic ``compensations`` property

    This expects a single compensation to be present and requires the
    following properties be available:

    * ``compensation_type``
    * ``hire_date``
    * ``compensation``
    """
    @property
    def compensations(self):
        return [
            {
                'tx_salaries.CompensationType': {
                    'name': self.compensation_type,
                },
                'tx_salaries.EmployeeTitle': {
                    'name': self.job_title,
                },
                'tx_salaries.Employee': {
                    'hire_date': self.hire_date,
                    'compensation': self.compensation,
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
            r['gender'] = self.get_mapped_value('gender')

        return r


class RaceMixin(object):
    """
    Adds a generic ``race`` property that assumes only a simple race name

    Requires a ``race`` property to be available.
    """
    @property
    def given_race(self):
        return {
            'name': self.get_mapped_value('race')
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
    and ``CLASSICATION_TYPE`` properties of the main level agency or
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
