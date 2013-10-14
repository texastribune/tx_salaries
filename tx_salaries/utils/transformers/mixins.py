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

