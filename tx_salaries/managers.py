from django.db import models


class DenormalizeManagerMixin(object):
    def update_cohort(self, cohort, **kwargs):
        stats, created = self.get_or_create(**kwargs)
        total_in_cohort = cohort.count()
        stats.highest_paid = cohort.order_by('-compensation')[0]
        stats.median_paid = cohort.order_by('-compensation')[(total_in_cohort - 1) / 2]
        stats.lowest_paid = cohort.order_by('compensation')[0]
        stats.races = self.get_races(cohort)
        stats.female = self.generate_stats(cohort.filter(
                                           position__person__gender='F'), True)
        stats.male = self.generate_stats(cohort.filter(
                                         position__person__gender='M'), True)
        stats.time_employed = self.get_tenures(cohort)
        stats.total_number = total_in_cohort
        stats.save()

    def generate_stats(self, cohort, get_slices=False):
        total_number = cohort.count()
        if total_number > 0:

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
            data = {
                'highest_paid': (cohort.order_by('-compensation')
                                       .values_list('compensation', flat=True)[0]),
                'median_paid': median_paid,
                'lowest_paid': (cohort.order_by('compensation')
                                      .values_list('compensation', flat=True)[0]),
                'total_number': total_number
            }
            if get_slices:
                data.update({'distribution': self.get_distribution(cohort)})
            return data
        else:
            return {'total_number': 0}

    def get_races(self, cohort):
        unique_races = (cohort.values_list('position__person__races__name',
                                           flat=True).distinct())
        data = []
        for race in unique_races:
            race_cohort = cohort.filter(position__person__races__name=race)
            data.append({
                'race': race,
                'stats': self.generate_stats(race_cohort)
            })
        return data

    def get_tenures(self, cohort):
        one_year = cohort.filter(hire_date__gte='2014-01-01')
        five_years = (cohort.filter(hire_date__lt='2014-01-01',
                                    hire_date__gte='2009-01-01'))
        ten_years = (cohort.filter(hire_date__lt='2009-01-01',
                                   hire_date__gte='2004-01-01'))
        twenty_years = cohort.filter(hire_date__lt='2004-01-01')
        return [
            {'time': '1 year', 'stats': self.generate_stats(one_year)},
            {'time': '5-10 years', 'stats': self.generate_stats(five_years)},
            {'time': '10-20 years', 'stats': self.generate_stats(ten_years)},
            {'time': '20+ years', 'stats': self.generate_stats(twenty_years)}
        ]

    def round_nearest(self, num, target, ceil=False, floor=False):
        num = int(num)
        if floor or (not ceil and num % target < target / 2):
            return num - (num % target)
        else:
            return num + (target - num % target)

    def get_distribution(self, cohort):
        if cohort.count() == 0:
            return None
        # Set bounds of buckets using all employees so breakdowns are comparable
        salaries = cohort.aggregate(
                        max=models.Max('compensation'),
                        min=models.Min('compensation'))
        diff = salaries['max'] - salaries['min']
        if diff == 0:
            # TODO test
            return {
                'step': 0,
                'slices': [{
                    'start': salaries['min'],
                    'end': salaries['max'],
                    'count': cohort.count()
                }]
            }
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
                'count': cohort.filter(compensation__gt=start,
                                       compensation__lte=start+step).count(),
            })
            start += step
        if not slices:
            return None
        slices[0]['count'] += cohort.filter(compensation=salaries['min']).count()

        return {'step': step, 'slices': slices}


class OrganizationStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
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
        self.update_cohort(cohort, organization=obj)


class PositionStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        from tx_salaries.models import Employee
        position_cohort = Employee.objects.filter(
                position__organization=obj.organization,
                position__post=obj)
        self.update_cohort(position_cohort, position=obj)


class EmployeeTitleStatsManager(DenormalizeManagerMixin, models.Manager):
    use_for_related_manager = True

    def denormalize(self, obj):
        self.update_cohort(obj.title.employees.all(), title=obj.title)
