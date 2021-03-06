from django.core import management
from django.test import TestCase

from tx_salaries.factories import (OrganizationFactory, PostFactory,
                                   MembershipFactory, EmployeeFactory,
                                   CompensationTypeFactory)

from tx_salaries.models import OrganizationStats, PositionStats


class DenormalizeCreatesStats(TestCase):
    def test_no_stats_without_denormalize(self):
        parent_org = OrganizationFactory(name="Test Parent")
        child_org = OrganizationFactory(name="Test Child", parent=parent_org)

        post = PostFactory(organization=child_org)

        # POST MUST HAVE UNICODE VALUE
        membership = MembershipFactory(post=post, organization=child_org)
        full_time = CompensationTypeFactory(name='FT')

        employee = EmployeeFactory(position=membership,
                                   compensation_type=full_time)

        with self.assertRaises(OrganizationStats.DoesNotExist):
            parent_org.stats
            child_org.stats

        with self.assertRaises(PositionStats.DoesNotExist):
            post.stats

    def test_denormalize_creates_stats(self):
        parent_org = OrganizationFactory(name="Test Parent")
        child_org = OrganizationFactory(name="Test Child", parent=parent_org)

        post = PostFactory(organization=child_org)

        # POST MUST HAVE UNICODE VALUE
        membership = MembershipFactory(post=post, organization=child_org)
        full_time = CompensationTypeFactory(name='FT')

        employee = EmployeeFactory(position=membership,
                                   compensation_type=full_time)

        management.call_command('denormalize_salary_data')

        self.assertEqual(parent_org.stats.total_number, 1)
        self.assertEqual(child_org.stats.total_number, 1)
        self.assertEqual(post.stats.total_number, 1)
