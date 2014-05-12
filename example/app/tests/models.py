from django.test import TestCase
from tx_salaries.factories import OrganizationFactory, PostFactory, MembershipFactory, EmployeeFactory


class EvenEmployeeMedianTest(TestCase):
    def test_update_cohort(self):
        organization = OrganizationFactory(name="Test Organization")
        post = PostFactory(organization=organization)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=organization,
                                           person__gender='F')
        membership_two = MembershipFactory(post=post, organization=organization,
                                           person__gender='F')

        # create two employees
        employee_one = EmployeeFactory(compensation=135000,
                                       position=membership_one)
        employee_two = EmployeeFactory(compensation=62217,
                                       position=membership_two)

        # assert median salary of the organization is 98608.5
        self.assertEqual(
            organization.stats.female['median_paid']['compensation'], 98608.5)

        # and the total number of female employees is 2
        self.assertEqual(organization.stats.female['total_number'], 2)
