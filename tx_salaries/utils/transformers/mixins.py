from . import base


def title_case_property(key):
    """Simple property for title casing a mapped value"""
    return property(lambda self: self.get_mapped_value(key).title())


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

    This requires that the class mixing it in adds an
    ``ORGANIZATION_NAME`` property of the main level agency or
    department and needs a ``department`` property.
    """
    @property
    def organization(self):
        return {
            'name': self.ORGANIZATION_NAME,
            'children': [{
                'name': unicode(self.department),
            }],
        }


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
