from django.db import models
from tx_people import fields
from tx_people.models import Membership, Organization, Post

from . import managers
from . import mixins


def get_top_level_departments():
    """
    Utility function for getting top-level organizations

    This is a helper for querying the tx_people.Organization model.  It
    simply looks for all top-level organizations that have at least one
    employee associated with one of their children.  Once the queryset
    is retrieved, you can continue filtering, ordering, and so as you
    please.

    Note: This only works for the current situation of non-nested
    departments.
    """
    return (Organization.objects.select_related('stats')
            .filter(parent=None)
            .exclude(children__members__employee=None))


class CompensationType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    # TODO
    # calculator = models.CharField(choices=constants.AVAILABLE_CALCULATORS)

    def __unicode__(self):
        return self.name


class EmployeeTitle(models.Model):
    """
    Provides a unique title that there will only be one of.

    Unlike the tx_people `Membership` and `Post` models, this model is
    completely independent of any organization.  This allows comparison
    between and Associate Professor at El Paso Community College and
    Collin College without having to do aggregate queries across their
    respective memberships or posts.
    """
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class Employee(mixins.DenormalizeOnSaveMixin, mixins.TimeTrackingMixin,
        mixins.ReducedDateStartAndEndMixin, models.Model):
    """
    # TODO

    This uses the tx_people.Membership model to represent the
    relationship between a Person and an Organization.  The Membership
    contains all title information and those Membership instances can
    be a part of a particular Post.

    For example, consider Alice President.  She is the President of the
    University of Texas at Sometown, has an annual salary of $100k, and
    was hired in December of 2034.  The following models must be
    created or used to represent that:

    ``Person``
        Alice President
    ``Organization``
        University of Sometown
    ``Post``
        For President connected to the ``Organization``
    ``Membership``
        Connecting the ``Person``, ``Organizations`` and the ``Post``
    ``CompensationType``
        Full-Time Employee
    ``Employee``
        Connects to ``Membership``, has a ``start_date`` of ``2034-12``,
        a ``compensation`` of ``100000`` and connected to the
        appropriate ``CompensationType``.
    """
    position = models.ForeignKey(Membership)
    title = models.ForeignKey(EmployeeTitle, related_name='employees', null=True)
    hire_date = fields.ReducedDateField()
    compensation = models.DecimalField(decimal_places=4, max_digits=12)
    compensation_type = models.ForeignKey(CompensationType)

    def __unicode__(self):
        return u'{title}, {person}'.format(title=self.position.post,
                person=self.position.person)


def create_stats_mixin(prefix):
    def generate_kwargs(field):
        return {
            'related_name': '{0}_stats_{1}'.format(prefix, field),
            'null': True,
            'blank': True,
        }

    class StatisticsMixin(models.Model):
        highest_paid = models.ForeignKey('Employee', **generate_kwargs('highest'))
        median_paid = models.ForeignKey('Employee', **generate_kwargs('median'))
        lowest_paid = models.ForeignKey('Employee', **generate_kwargs('lowest'))
        total_number = models.PositiveIntegerField(default=0)

        class Meta:
            abstract = True

    return StatisticsMixin


class EmployeeTitleStats(create_stats_mixin('title'), models.Model):
    title = models.OneToOneField(EmployeeTitle, related_name='stats')

    objects = managers.EmployeeTitleStatsManager()


class PositionStats(create_stats_mixin('position'), models.Model):
    position = models.OneToOneField(Post, related_name='stats')

    objects = managers.PositionStatsManager()

    def generate_stats(self, cohort, get_slices=False):
        # TODO this dict is not ideal
        total_number = cohort.count()
        if total_number > 0:
            data = {
                'highest_paid': self.get_employee(cohort
                                    .order_by('-employee__compensation')
                                    .values('employee__id')[0]),
                'median_paid': self.get_employee(cohort
                                    .order_by('-employee__compensation')
                                    .values('employee__id')[(total_number - 1) / 2]),
                'lowest_paid': self.get_employee(cohort
                                    .order_by('employee__compensation')
                                    .values('employee__id')[0]),
                'total_number': total_number
            }
            if get_slices:
                data.update({'distribution': self.get_distribution(cohort)})
            return data
        else:
            return {'total_number': 0}

    def round_nearest(self, num, target, ceil=False, floor=False):
        num = int(num)
        if floor or (not ceil and num % target < target / 2):
            return num - (num % target)
        else:
            return num + (target - num % target)

    def get_distribution(self, cohort):
        if cohort.count() <= 1:
            return None
        # Set bounds of buckets using all employees so breakdowns are comparable
        salaries = self.position.organization.members.aggregate(
                        max=models.Max('employee__compensation'),
                        min=models.Min('employee__compensation'))
        diff = salaries['max'] - salaries['min']
        step = diff / 10
        start = salaries['min']

        # Round start and step to nice numbers, and make the step bigger if
        # it would create more than 12 bars on the graph.
        if step > 70000 or diff / 50000 > 12:
            step = self.round_nearest(step, 100000, ceil=True)
            start = self.round_nearest(start, 100000, floor=True)
        elif step > 30000 or diff / 20000 > 12:
            step = 50000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 15000 or diff / 10000 > 12:
            step = 20000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 8000 or diff / 5000 > 12:
            step = 10000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 3000:
            step = 5000
            start = self.round_nearest(start, 1000, floor=True)
        elif step > 70:
            step = self.round_nearest(step, 100)
            start = self.round_nearest(start, 100, floor=True)

        slices = []
        while start < salaries['max']:
            slices.append({
                'start': start,
                'end': start + step,
                'count': cohort.filter(employee__compensation__gt=start,
                                        employee__compensation__lte=start+step).count(),
            })
            start += step
        if not slices:
            return None
        slices[0]['count'] += cohort.filter(employee__compensation=salaries['min']).count()

        return {'step': step, 'slices': slices}

    def get_employee(self, employee):
        # TODO this lookup is also not ideal
        return Employee.objects.get(id=employee['employee__id'])

    @property
    def female(self):
        females = self.position.members.filter(person__gender='F')
        return self.generate_stats(females, True)

    @property
    def male(self):
        males = self.position.members.filter(person__gender='M')
        return self.generate_stats(males, True)

    @property
    def races(self):
        unique_races = (self.position.members
                                .values_list('person__races__name', flat=True)
                                .distinct())
        data = []
        for race in unique_races:
            race_cohort = self.position.members.filter(person__races__name=race)
            data.append({
                'race': race,
                'stats': self.generate_stats(race_cohort)
            })
        return data

    @property
    def time_employed(self):
        # TODO
        one_year = self.position.members.filter(employee__hire_date__gte='2014-01-01')
        five_years = (self.position.members.filter(employee__hire_date__lt='2014-01-01',
                                        employee__hire_date__gte='2009-01-01'))
        ten_years = (self.position.members.filter(employee__hire_date__lt='2009-01-01',
                                        employee__hire_date__gte='2004-01-01'))
        twenty_years = self.position.members.filter(employee__hire_date__lt='2004-01-01')
        return [
            {'time': '1 year', 'stats': self.generate_stats(one_year)},
            {'time': '5-10 years', 'stats': self.generate_stats(five_years)},
            {'time': '10-20 years', 'stats': self.generate_stats(ten_years)},
            {'time': '20+ years', 'stats': self.generate_stats(twenty_years)},
        ]


class OrganizationStats(create_stats_mixin('organization'),
        models.Model):
    organization = models.OneToOneField(Organization, related_name='stats')

    objects = managers.OrganizationStatsManager()

    def generate_stats(self, cohort, get_slices=False):
        # TODO this dict is not ideal
        total_number = cohort.count()
        if total_number > 0:
            data = {
                'highest_paid': self.get_employee(cohort
                                    .order_by('-employee__compensation')
                                    .values('employee__id')[0]),
                'median_paid': self.get_employee(cohort
                                    .order_by('-employee__compensation')
                                    .values('employee__id')[(total_number - 1) / 2]),
                'lowest_paid': self.get_employee(cohort
                                    .order_by('employee__compensation')
                                    .values('employee__id')[0]),
                'total_number': total_number
            }
            if get_slices:
                data.update({'distribution': self.get_distribution(cohort)})
            return data
        else:
            return {'total_number': 0}

    def round_nearest(self, num, target, ceil=False, floor=False):
        num = int(num)
        if floor or (not ceil and num % target < target / 2):
            return num - (num % target)
        else:
            return num + (target - num % target)

    def get_distribution(self, cohort):
        if cohort.count() <= 1:
            return None
        # Set bounds of buckets using all employees so breakdowns are comparable
        salaries = self.organization.members.aggregate(
                        max=models.Max('employee__compensation'),
                        min=models.Min('employee__compensation'))
        diff = salaries['max'] - salaries['min']
        step = diff / 10
        start = salaries['min']

        # Round start and step to nice numbers, and make the step bigger if
        # it would create more than 12 bars on the graph.
        if step > 70000 or diff / 50000 > 12:
            step = self.round_nearest(step, 100000, ceil=True)
            start = self.round_nearest(start, 100000, floor=True)
        elif step > 30000 or diff / 20000 > 12:
            step = 50000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 15000 or diff / 10000 > 12:
            step = 20000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 8000 or diff / 5000 > 12:
            step = 10000
            start = self.round_nearest(start, 10000, floor=True)
        elif step > 3000:
            step = 5000
            start = self.round_nearest(start, 1000, floor=True)
        elif step > 70:
            step = self.round_nearest(step, 100)
            start = self.round_nearest(start, 100, floor=True)

        slices = []
        while start < salaries['max']:
            slices.append({
                'start': start,
                'end': start + step,
                'count': cohort.filter(employee__compensation__gt=start,
                                        employee__compensation__lte=start+step).count(),
            })
            start += step
        if not slices:
            return None
        slices[0]['count'] += cohort.filter(employee__compensation=salaries['min']).count()

        return {'step': step, 'slices': slices}

    def get_employee(self, employee):
        # TODO this lookup is also not ideal
        return Employee.objects.get(id=employee['employee__id'])

    @property
    def female(self):
        cohort = self.organization.members.filter(person__gender='F')
        return self.generate_stats(cohort, True)

    @property
    def male(self):
        cohort = self.organization.members.filter(person__gender='M')
        return self.generate_stats(cohort, True)

    @property
    def races(self):
        unique_races = (self.organization.members
                                .values_list('person__races__name', flat=True)
                                .distinct())
        data = []
        for race in unique_races:
            race_cohort = self.organization.members.filter(person__races__name=race)
            data.append({
                'race': race,
                'stats': self.generate_stats(race_cohort)
            })
        return data

    @property
    def time_employed(self):
        # TODO use dates on the models, don't calculate off jan. 1
        one_year = self.organization.members.filter(employee__hire_date__gte='2014-01-01')
        five_years = (self.organization.members.filter(employee__hire_date__lt='2014-01-01',
                                        employee__hire_date__gte='2009-01-01'))
        ten_years = (self.organization.members.filter(employee__hire_date__lt='2009-01-01',
                                        employee__hire_date__gte='2004-01-01'))
        twenty_years = self.organization.members.filter(employee__hire_date__lt='2004-01-01')
        return [
            {'time': '1 year', 'stats': self.generate_stats(one_year)},
            {'time': '5-10 years', 'stats': self.generate_stats(five_years)},
            {'time': '10-20 years', 'stats': self.generate_stats(ten_years)},
            {'time': '20+ years', 'stats': self.generate_stats(twenty_years)},
        ]
