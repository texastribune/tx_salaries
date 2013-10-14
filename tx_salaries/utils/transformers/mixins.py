class OrganizationMixin(object):
    @property
    def organization(self):
        return {
            'name': self.ORGANIZATION_NAME,
            'children': [{
                'name': unicode(self.department),
            }],
        }

