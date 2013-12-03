from django.db import models


class DenormalizeManagerMixin(object):
    def update_cohort(self, cohort, **kwargs):
        stats, created = self.get_or_create(**kwargs)
        stats.highest_paid = cohort.order_by('-compensation')[0]
        stats.lowest_paid = cohort.order_by('compensation')[0]
        stats.save()


class OrganizationStatsManager(models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        Employee = obj._meta.concrete_model
        use_children = False
        organization = obj.position.organization

        # TODO: Allow organization to break and say it is top-level
        #       Example: El Paso County Sheriff's Department instead
        #       of going all the way to El Paso County.
        if organization.parent:
            use_children = True
            organization = organization.parent

        if use_children:
            kwargs = {
                'parent': None,
                'children__members__employee': obj,
            }
        else:
            kwargs = {'members__employee': obj, }

        cohort = Employee.objects.filter(**kwargs)

        self.update_cohort(cohort, organization=organization)


class PositionStatsManager(models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        Employee = obj._meta.concrete_model
        position_cohort = Employee.objects.filter(
                position__organization=obj.position.organization)
        self.update_cohort(position_cohort, position=obj.position.post)
