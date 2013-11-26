from django.db import models


class PositionStatsManager(models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        Employee = obj._meta.concrete_model
        position_cohort = Employee.objects.filter(
                position__organization=obj.position.organization)
        stats, created = self.get_or_create(
                position=obj.position.post)
        stats.highest_paid = position_cohort.order_by('-compensation')[0]
        stats.lowest_paid = position_cohort.order_by('compensation')[0]
        stats.save()
