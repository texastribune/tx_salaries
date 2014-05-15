from django.test import TestCase
from tx_salaries.factories import OrganizationFactory, PostFactory, MembershipFactory, EmployeeFactory


class ParentAndChildHaveStats(TestCase):
    def test_parent_child_have_stats(self):
        parent_org = OrganizationFactory(name="Test Parent")
        child_org = OrganizationFactory(name="Test Child", parent=parent_org)

        post = PostFactory(organization=child_org)

        # POST MUST HAVE UNICODE VALUE
        membership = MembershipFactory(post=post, organization=child_org)

        employee = EmployeeFactory(position=membership)

        self.assertTrue(parent_org.stats)
        self.assertTrue(child_org.stats)
