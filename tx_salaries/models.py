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

    def generate_stats(self, cohort):
        # TODO this dict is not ideal
        total_number = cohort.count()
        if total_number > 0:
            return {
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
        # return false if cohort is empty because stats cannot be calculated
        return False

    def get_employee(self, employee):
        # TODO this lookup is also not ideal
        return Employee.objects.get(id=employee['employee__id'])

    @property
    def female(self):
        females = self.position.members.filter(person__gender='F')
        return self.generate_stats(females)

    @property
    def male(self):
        males = self.position.members.filter(person__gender='M')
        return self.generate_stats(males)


class OrganizationStats(create_stats_mixin('organization'),
        models.Model):
    organization = models.OneToOneField(Organization, related_name='stats')

    objects = managers.OrganizationStatsManager()

    def generate_stats(self, cohort):
        # TODO this dict is not ideal
        total_number = cohort.count()
        if total_number > 0:
            return {
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
        # return false if cohort is empty because stats cannot be calculated
        return False

    def get_employee(self, employee):
        # TODO this lookup is also not ideal
        return Employee.objects.get(id=employee['employee__id'])

    @property
    def female(self):
        females = self.organization.members.filter(person__gender='F')
        return self.generate_stats(females)

    @property
    def male(self):
        males = self.organization.members.filter(person__gender='M')
        return self.generate_stats(males)
