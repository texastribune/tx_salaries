from django.db import models


class DenormalizeManagerMixin(object):
    def update_cohort(self, cohort, **kwargs):
        stats, created = self.get_or_create(**kwargs)
        total_in_cohort = cohort.count()
        stats.highest_paid = cohort.order_by('-compensation')[0]
        stats.median_paid = cohort.order_by('-compensation')[(total_in_cohort - 1) / 2]
        stats.lowest_paid = cohort.order_by('compensation')[0]
        stats.total_number = cohort.count()
        stats.save()


class OrganizationStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        Employee = obj._meta.concrete_model
        use_children = False
        organization = obj.position.organization

        # TODO: Allow organization to break and say it is top-level
        #       Example: El Paso County Sheriff's Department instead
        #       of going all the way to El Paso County.
        # if organization.parent:
        #     use_children = True
        #     organization = organization.parent

        if use_children:
            kwargs = {'position__organization__parent': organization, }
        else:
            kwargs = {'position__organization': organization, }

        cohort = Employee.objects.filter(**kwargs)

        self.update_cohort(cohort, organization=organization)


class PositionStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        Employee = obj._meta.concrete_model
        position_cohort = Employee.objects.filter(
                position__organization=obj.position.organization,
                position__post=obj.position.post)
        self.update_cohort(position_cohort, position=obj.position.post)


class EmployeeTitleStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        self.update_cohort(obj.title.employees.all(), title=obj.title)
