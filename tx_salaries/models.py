from datetime import datetime

from django.db import models
from django.utils.text import slugify
from tx_people import fields
from tx_people.models import Membership, Organization, Post
from tx_people import mixins
from django.contrib.postgres.fields import JSONField

from . import managers


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
    return Organization.objects.filter(parent=None, stats__isnull=False)


class CompensationType(models.Model):
    """
    Classification of a compensation

    Only compensations with name == ``FT`` are denormalized. The
    ``description`` field is displayed to users on the web app.
    """
    name_choices = (
        ('FT', 'Full Time'),
        ('PT', 'Part Time')
    )
    name = models.CharField(max_length=250, choices=name_choices)
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


class Employee(mixins.TimeTrackingMixin, mixins.ReducedDateStartAndEndMixin,
               models.Model):
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
    tenure = models.DecimalField(null=True, blank=True, decimal_places=2,
                                 max_digits=12)
    slug = models.SlugField(max_length=255, null=True, blank=True, default=None)
    compensation = models.DecimalField(
        decimal_places=2, max_digits=12, db_index=True)
    compensation_type = models.ForeignKey(CompensationType)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{title}, {person}'.format(title=self.position.post,
                person=self.position.person)

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.position.person.name))
        super(Employee, self).save(*args, **kwargs)

    @property
    def hire_date_as_date(self):
        return datetime.strptime(self.hire_date, '%Y-%m-%d')


def create_stats_mixin(prefix):
    def generate_kwargs(field):
        # Default options for ``DecimalField`` models
        return {
            'null': True,
            'blank': True,
            'decimal_places': 2,
            'max_digits': 12
        }

    class StatisticsMixin(models.Model):
        """
        ``PositionStats`` and ``OrganizationStats`` models inherit these fields
        """
        distribution = JSONField(null=True)
        highest_paid = models.DecimalField(**generate_kwargs('highest'))
        median_paid = models.DecimalField(**generate_kwargs('median'))
        lowest_paid = models.DecimalField(**generate_kwargs('lowest'))
        total_number = models.PositiveIntegerField(default=0)
        races = JSONField(null=True)
        female = JSONField(null=True)
        male = JSONField(null=True)
        time_employed = JSONField(null=True)
        date_provided = models.DateField(null=True, blank=True)
        slug = models.SlugField(max_length=255, null=True, blank=True,
                                default=None)

        class Meta:
            abstract = True

    return StatisticsMixin


class PositionStats(create_stats_mixin('position'), models.Model):
    position = models.OneToOneField(Post, related_name='stats')

    objects = managers.PositionStatsManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.position.label))
        super(PositionStats, self).save(*args, **kwargs)


class OrganizationStats(create_stats_mixin('organization'), models.Model):
    organization = models.OneToOneField(Organization, related_name='stats')

    objects = managers.OrganizationStatsManager()

    def save(self, *args, **kwargs):
        self.slug = slugify(unicode(self.organization.name))
        super(OrganizationStats, self).save(*args, **kwargs)
