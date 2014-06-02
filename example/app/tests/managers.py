from django.core import management
from django.test import TestCase
from datetime import date

from tx_salaries.factories import (OrganizationFactory, PostFactory,
                                   MembershipFactory, EmployeeFactory)


class EvenEmployeeMedianTest(TestCase):
    def test_gender_breakdown(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        membership_two = MembershipFactory(post=post, organization=department,
                                           person__gender='F')

        # create two employees
        employee_one = EmployeeFactory(compensation=135000,
                                       position=membership_one)
        employee_two = EmployeeFactory(compensation=62217,
                                       position=membership_two)
        management.call_command('denormalize_salary_data')
        # assert median salary of the organization is 98608.5
        self.assertEqual(
            float(department.stats.female['median_paid']), 98608.5)

        # and the total number of female employees is 2
        self.assertEqual(department.stats.female['total_number'], 2)

    def test_department_stats(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        membership_two = MembershipFactory(post=post, organization=department,
                                           person__gender='F')

        # create two employees
        employee_one = EmployeeFactory(compensation=135000,
                                       position=membership_one)
        employee_two = EmployeeFactory(compensation=62217,
                                       position=membership_two)
        management.call_command('denormalize_salary_data')
        self.assertEqual(department.stats.median_paid, 98608.5)


class RatiosAddUpTest(TestCase):
    def test_gender_ratios(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        membership_two = MembershipFactory(post=post, organization=department,
                                           person__gender='F')

        membership_three = MembershipFactory(post=post, organization=department,
                                             person__gender='M')

        membership_four = MembershipFactory(post=post, organization=department,
                                            person__gender='M')
        female_one = EmployeeFactory(compensation=135000,
                                       position=membership_one)
        female_two = EmployeeFactory(compensation=62217,
                                       position=membership_two)
        male_one = EmployeeFactory(compensation=140000,
                                   position=membership_three)
        male_two = EmployeeFactory(compensation=61050, position=membership_four)

        management.call_command('denormalize_salary_data')

        self.assertEqual(department.stats.male['ratio'] + department.stats.female['ratio'], 100)

    def calculate_tenure(self, hire_date, date_provided):
        hire_date_data = map(int, hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        return float((date_provided - hire_date).days) / float(360)

    def test_time_employed(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        membership_two = MembershipFactory(post=post, organization=department,
                                           person__gender='F')

        membership_three = MembershipFactory(post=post, organization=department,
                                             person__gender='M')

        membership_four = MembershipFactory(post=post, organization=department,
                                            person__gender='M')
        female_one = EmployeeFactory(compensation=135000,
                                       position=membership_one,
                                       tenure=self.calculate_tenure('1975-04-10', date.today()))
        female_two = EmployeeFactory(compensation=62217,
                                       position=membership_two,
                                       tenure=self.calculate_tenure('1985-04-10', date.today()))
        male_one = EmployeeFactory(compensation=140000,
                                   position=membership_three,
                                   tenure=self.calculate_tenure('2012-04-10', date.today()))
        male_two = EmployeeFactory(compensation=61050, position=membership_four,
                                   tenure=self.calculate_tenure('1995-04-10', date.today()))

        management.call_command('denormalize_salary_data')

        tenure_ratio_sum = 0
        for t in department.stats.time_employed:
            try:
                tenure_ratio_sum += t['stats']['ratio']
            except KeyError:
                continue
        self.assertEqual(tenure_ratio_sum, 100)
