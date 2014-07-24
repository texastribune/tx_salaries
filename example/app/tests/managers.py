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

        male_ratio_sum = sum([b['ratio'] for b in department.stats.male['distribution']['slices']])
        self.assertEqual(male_ratio_sum, department.stats.male['ratio'])
        self.assertEqual(department.stats.male['ratio'], 50)

        female_ratio_sum = sum([b['ratio'] for b in department.stats.female['distribution']['slices']])
        self.assertEqual(female_ratio_sum, department.stats.female['ratio'])
        self.assertEqual(department.stats.female['ratio'], 50)

        self.assertEqual(department.stats.male['ratio'] + department.stats.female['ratio'], 100)

    def calculate_tenure(self, hire_date, date_provided):
        hire_date_data = map(int, hire_date.split('-'))
        hire_date = date(hire_date_data[0], hire_date_data[1],
                         hire_date_data[2])
        tenure = float((date_provided - hire_date).days) / float(360)
        if tenure < 0:
            error_msg = ("An employee was hired after the data was provided.\n"
                         "Is DATE_PROVIDED correct?")
            raise ValueError(error_msg)
        return tenure

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

        management.call_command('denormalize_salary_data')

        tenure_ratio_sum = 0
        for t in department.stats.time_employed:
            try:
                tenure_ratio_sum += t['stats']['ratio']
            except KeyError:
                continue
        self.assertEqual(tenure_ratio_sum, 100)

        with self.assertRaises(ValueError):
            EmployeeFactory(compensation=61050, position=membership_four,
                            tenure=self.calculate_tenure('1995-04-10', date(1900, 1, 1)))

    def test_gender_histogram(self):
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
        female_two = EmployeeFactory(compensation=162217,
                                       position=membership_two)
        male_one = EmployeeFactory(compensation=140000,
                                   position=membership_three)
        male_two = EmployeeFactory(compensation=61050, position=membership_four)

        management.call_command('denormalize_salary_data')

        male_sum = sum([b['count'] for b in department.stats.male['distribution']['slices']])
        self.assertEqual(male_sum, department.stats.male['total_number'])

        female_sum = sum([b['count'] for b in department.stats.female['distribution']['slices']])
        self.assertEqual(female_sum, department.stats.female['total_number'])

        self.assertEqual(department.stats.female['distribution']['slices'][0]['start'],
                         department.stats.male['distribution']['slices'][0]['start'])

    def test_overall_distribution(self):
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
        female_two = EmployeeFactory(compensation=162217,
                                       position=membership_two)
        male_one = EmployeeFactory(compensation=140000,
                                   position=membership_three)
        male_two = EmployeeFactory(compensation=61050, position=membership_four)

        management.call_command('denormalize_salary_data')
        self.assertTrue(parent_org.stats.distribution)
        self.assertTrue(department.stats.distribution)

        slice_sum = sum([b['count'] for b in department.stats.distribution['slices']])
        self.assertEqual(slice_sum, department.stats.total_number)

        parent_slice_sum = sum([b['count'] for b in parent_org.stats.distribution['slices']])
        self.assertEqual(slice_sum, parent_org.stats.total_number)

    def test_empty_cohort(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        female_one = EmployeeFactory(compensation=135000,
                                     position=membership_one)
        management.call_command('denormalize_salary_data')

        self.assertTrue(parent_org.stats.male['distribution'])
        self.assertTrue(department.stats.distribution)

        male_slice_sum = sum([b['count'] for b in department.stats.male['distribution']['slices']])
        self.assertEqual(male_slice_sum, 0)

    def test_salary_in_correct_bin(self):
        '''
        Based on UT Brownsville's Office of the President,
        which misplaced president's salary prior to managers.py change
        '''
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        president = EmployeeFactory(compensation=311783,
                                       position=membership_one)
        female_two = EmployeeFactory(compensation=108000,
                                       position=membership_one)
        female_three = EmployeeFactory(compensation=96256,
                                       position=membership_one)
        female_four = EmployeeFactory(compensation=70000,
                                       position=membership_one)
        female_five = EmployeeFactory(compensation=65000,
                                       position=membership_one)
        female_six = EmployeeFactory(compensation=47815,
                                       position=membership_one)
        male_one = EmployeeFactory(compensation=34000,
                                   position=membership_one)
        male_two = EmployeeFactory(compensation=26663, position=membership_one)

        management.call_command('denormalize_salary_data')

        slice_length = len(department.stats.distribution['slices'])
        last_slice = department.stats.distribution['slices'][slice_length - 1]
        max_end = max([s['end'] for s in department.stats.distribution['slices']])
        self.assertEqual(max_end, last_slice['end'])
        self.assertTrue(president.compensation <= last_slice['end'])
        self.assertTrue(president.compensation > last_slice['start'])

    def test_no_diff_distribution(self):
        parent_org = OrganizationFactory(name="Test Parent Organization")
        department = OrganizationFactory(name="Test Organization",
                                           parent=parent_org)
        post = PostFactory(organization=department)
        # POST MUST HAVE UNICODE VALUE
        membership_one = MembershipFactory(post=post, organization=department,
                                           person__gender='F')
        membership_three = MembershipFactory(post=post, organization=department,
                                             person__gender='M')
        female_one = EmployeeFactory(compensation=135000,
                                     position=membership_one)
        male_one = EmployeeFactory(compensation=135000, position=membership_three)
        management.call_command('denormalize_salary_data')

        self.assertEqual(parent_org.stats.distribution['step'], 0)
        self.assertEqual(department.stats.distribution['step'], 0)

        self.assertEqual(parent_org.stats.distribution['slices'][0]['start'],
                         department.stats.distribution['slices'][0]['end'])
        self.assertEqual(department.stats.distribution['slices'][0]['start'],
                         department.stats.distribution['slices'][0]['end'])

        self.assertEqual(department.stats.distribution['slices'][0]['ratio'], 100)
        self.assertEqual(parent_org.stats.male['distribution']['slices'][0]['ratio'], 50)
        self.assertEqual(parent_org.stats.female['distribution']['slices'][0]['ratio'], 50)
