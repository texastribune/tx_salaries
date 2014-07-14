from django.db import models


class DenormalizeManagerMixin(object):
    def update_cohort(self, cohort, date_provided=False, **kwargs):
        stats, created = self.get_or_create(**kwargs)
        total_in_cohort = cohort.count()
        stats.distribution = self.get_distribution(cohort, total_in_cohort, cohort)
        stats.highest_paid = (cohort.order_by('-compensation')
                                    .values_list('compensation', flat=True)[0])
        stats.median_paid = self.get_median(cohort, total_in_cohort)
        stats.lowest_paid = (cohort.order_by('compensation')
                                   .values_list('compensation', flat=True)[0])
        stats.races = self.get_races(cohort, total_in_cohort)
        stats.female = self.generate_stats(cohort.filter(
                                           position__person__gender='F'),
                                           total_in_cohort, True, cohort)
        stats.male = self.generate_stats(cohort.filter(
                                         position__person__gender='M'),
                                         total_in_cohort, True, cohort)
        stats.time_employed = self.get_tenures(cohort, total_in_cohort)
        stats.total_number = total_in_cohort
        if date_provided:
            stats.date_provided = date_provided
        stats.save()

    def get_median(self, cohort, total_number):
        if total_number % 2 == 0:
            median_paid = (
                (cohort.order_by('-compensation')
                       .values_list('compensation',
                                    flat=True)[(total_number / 2)] +
                 cohort.order_by('-compensation')
                       .values_list('compensation',
                                    flat=True)[(total_number / 2) - 1]) / 2)
        else:
            median_paid = (cohort.order_by('-compensation')
                                 .values_list('compensation',
                                              flat=True)[(total_number - 1) / 2])
        return median_paid

    def generate_stats(self, cohort, total_in_cohort, get_slices=False,
                       parent_cohort=False):
        total_number = cohort.count()
        if total_number > 0:
            data = {
                'highest_paid': (cohort.order_by('-compensation')
                                       .values_list('compensation', flat=True)[0]),
                'median_paid': self.get_median(cohort, total_number),
                'lowest_paid': (cohort.order_by('compensation')
                                      .values_list('compensation', flat=True)[0]),
                'total_number': total_number,
                'ratio': round((float(total_number) / float(total_in_cohort)) * 100, 1)
            }

        else:
            data = {'total_number': 0}

        if get_slices:
            data.update({'distribution': self.get_distribution(cohort,
                                                               total_in_cohort,
                                                               parent_cohort)})
        return data

    def get_races(self, cohort, total_in_cohort):
        unique_races = (cohort.values_list('position__person__races__name',
                                           flat=True).distinct())
        data = []
        for race in unique_races:
            race_cohort = cohort.filter(position__person__races__name=race)
            data.append({
                'race': race,
                'stats': self.generate_stats(race_cohort, total_in_cohort)
            })
        return data

    def get_tenures(self, cohort, total_in_cohort):
        one_year = cohort.filter(tenure__lte=1)
        more_than_one_year = (cohort.filter(tenure__lt=10,
                                            tenure__gt=1))
        ten_years = (cohort.filter(tenure__lt=20,
                                   tenure__gte=10))
        twenty_years = cohort.filter(tenure__gt=20)
        return [
            {'time': '1 year', 'stats': self.generate_stats(one_year, total_in_cohort)},
            {'time': '1-10 years', 'stats': self.generate_stats(more_than_one_year, total_in_cohort)},
            {'time': '10-20 years', 'stats': self.generate_stats(ten_years, total_in_cohort)},
            {'time': '20+ years', 'stats': self.generate_stats(twenty_years, total_in_cohort)}
        ]

    def round_nearest(self, num, target, ceil=False, floor=False):
        num = int(num)
        if floor or (not ceil and num % target < target / 2):
            return num - (num % target)
        else:
            return num + (target - num % target)

    def get_distribution(self, cohort, total_in_cohort, parent_cohort):
        # Set bounds of buckets using all employees so gender breakdowns are comparable
        salaries = parent_cohort.aggregate(max=models.Max('compensation'),
                                    min=models.Min('compensation'))
        diff = salaries['max'] - salaries['min']
        if diff == 0:
            # TODO test
            return {
                'step': 0,
                'slices': [{
                    'start': salaries['min'],
                    'end': salaries['max'],
                    'count': cohort.count(),
                    'ratio': round((float(cohort.count()) / float(total_in_cohort)) * 100, 1)
                }]
            }
        if cohort != parent_cohort:
            if diff == 0:
                step = diff / 1
            elif diff < 20000:
                step = diff / 3
            else:
                step = diff / 6
        else:
            step = diff/10

        start = salaries['min']

        slices = []
        while start < salaries['max']:
            if start == salaries['min']:
                cohort_total = (cohort.filter(compensation__gte=start,
                                              compensation__lte=start+step).count())
            else:
                cohort_total = (cohort.filter(compensation__gt=start,
                                              compensation__lte=start+step).count())
            slices.append({
                'start': start,
                'end': start + step,
                'count': cohort_total,
                'ratio': round((float(cohort_total) / float(total_in_cohort)) * 100, 1)
            })
            start += step
        if not slices:
            return None
        return {'step': step, 'slices': slices}


class OrganizationStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj, date_provided=False):
        from tx_salaries.models import Employee

        # TODO: Allow organization to break and say it is top-level
        #       Example: El Paso County Sheriff's Department instead
        #       of going all the way to El Paso County.
        if obj.parent:
            # employee works for a department,
            # also calculate parent organization stats
            kwargs = {'position__organization': obj, }

        else:
            kwargs = {'position__organization__parent': obj, }

        cohort = Employee.objects.filter(**kwargs)
        self.update_cohort(cohort, date_provided, organization=obj)


class PositionStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj, date_provided=False):
        from tx_salaries.models import Employee
        position_cohort = Employee.objects.filter(
                position__organization=obj.organization,
                position__post=obj)
        self.update_cohort(position_cohort, date_provided, position=obj)
