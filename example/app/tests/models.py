from django.core import management
from django.test import TestCase

from tx_salaries.factories import (OrganizationFactory, PostFactory,
                                   MembershipFactory, EmployeeFactory)


class GenerateSlugTest(TestCase):
    def test_employee_slug(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__name="Test Name",
                                           person__gender='F')
        female_one = EmployeeFactory(compensation=135000,
                                     position=membership_one)
        self.assertEqual(female_one.slug, 'test-name')

    def test_organization_slug(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__name="Test Name",
                                           person__gender='F')
        female_one = EmployeeFactory(compensation=135000,
                                     position=membership_one)

        management.call_command('denormalize_salary_data')

        self.assertEqual(department.stats.slug, 'test-organization')
        self.assertEqual(parent_org.stats.slug, 'test-parent-organization')
