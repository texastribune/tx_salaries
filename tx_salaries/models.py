from django.db import models
from tx_people import fields
from tx_people.models import Membership, Organization, Post

from . import managers
from . import mixins


class CompensationType(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    # TODO
    # calculator = models.CharField(choices=constants.AVAILABLE_CALCULATORS)

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
    hire_date = fields.ReducedDateField()
    compensation = models.DecimalField(decimal_places=4, max_digits=12)
    compensation_type = models.ForeignKey(CompensationType)

    def __unicode__(self):
        return u'{title}, {person}'.format(title=self.position.post,
                person=self.position.person)


def create_highest_lowest_mixin(prefix):
    def generate_kwargs(field):
        return {
            'related_name': '{0}_stats_{1}'.format(prefix, field),
            'null': True,
            'blank': True,
        }

    class HighestLowestMixin(models.Model):
        highest_paid = models.ForeignKey('Employee', **generate_kwargs('highest'))
        lowest_paid = models.ForeignKey('Employee', **generate_kwargs('lowest'))

        class Meta:
            abstract = True

    return HighestLowestMixin


class PositionStats(create_highest_lowest_mixin('position'), models.Model):
    position = models.ForeignKey(Post, related_name='stats')

    objects = managers.PositionStatsManager()


class OrganizationStats(create_highest_lowest_mixin('organization'),
        models.Model):
    organization = models.ForeignKey(Organization, related_name='stats')

    objects = managers.OrganizationStatsManager()
