from django.db import models
import math
import decimal

class DenormalizeManagerMixin(object):
    def update_cohort(self, cohort, date_provided=False, **kwargs):
        """
        Save each of the fields for ``PositionStats`` and ``OrganizationStats``
        models, which provide filtered ``Employee`` objects as the ``cohort``
        parameter
        """
        stats, created = self.get_or_create(**kwargs)
        total_in_cohort = cohort.count()
        # Overall distribution
        stats.distribution = self.get_distribution(cohort, total_in_cohort, cohort)
        stats.highest_paid = float(cohort.order_by('-compensation')
                                    .values_list('compensation', flat=True)[0])
        stats.median_paid = self.get_median(cohort)
        stats.lowest_paid = float(cohort.order_by('compensation')
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

    def get_median(self, cohort):
        """
        Calculate median salary for full-time employees of given cohort
        """
        cohort = cohort.filter(compensation_type__name='FT')
        total_number = cohort.count()
        if total_number == 0:
            # There are no full-time employees to calculate a median salary
            return None
        elif total_number % 2 == 0:
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
        return float(median_paid)

    def generate_stats(self, cohort, total_in_cohort, get_slices=False,
                       parent_cohort=False):
        """
        Calculate standard JSONField statistics

        Used by ``get_tenures``, ``get_races``, ``male`` and ``female``
        """
        total_number = cohort.count()
        if total_number > 0:
            median = self.get_median(cohort)
            data = {
                'highest_paid': float(cohort.order_by('-compensation')
                                       .values_list('compensation', flat=True)[0]),
                'median_paid': float(median) if median else None,
                'lowest_paid': float(cohort.order_by('compensation')
                                      .values_list('compensation', flat=True)[0]),
                'total_number': total_number,
                'ratio': round((float(total_number) / float(total_in_cohort)) * 100, 1)
            }

        else:
            data = {'total_number': 0}

        if get_slices:
            # Generate distribution for male and female histograms
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
            {'time': '1 year or less', 'stats': self.generate_stats(one_year, total_in_cohort)},
            {'time': '1-10 years', 'stats': self.generate_stats(more_than_one_year, total_in_cohort)},
            {'time': '10-20 years', 'stats': self.generate_stats(ten_years, total_in_cohort)},
            {'time': '20+ years', 'stats': self.generate_stats(twenty_years, total_in_cohort)}
        ]

    def round_nearest(self, num, target, ceil=False, floor=False):
        """
        Helper function rounding distribution bins
        """
        num = int(num)
        if floor or (not ceil and num % target < target / 2):
            return num - (num % target)
        else:
            return num + (target - num % target)

    def get_distribution(self, cohort, total_in_cohort, parent_cohort):
        parent_cohort_full_time = parent_cohort.filter(compensation_type__name='FT')
        cohort_full_time = cohort.filter(compensation_type__name='FT')
        if parent_cohort.count() == 0:
            # The entity has no full-time employees to generate a distribution
            return None

        # Set bounds of buckets using all employees so gender breakdowns are comparable
        salaries = parent_cohort_full_time.aggregate(max=models.Max('compensation'),
                                                     min=models.Min('compensation'))

        start = salaries['min']
        if start is None or start < 1200:
            start = 0
        else:
            start = int(math.floor(float(salaries['min'])/1200.0)) * 1200
        end = salaries['max']
        if end is None or end < 1200:
            end = 1200
        else:
            end = int(math.ceil(float(salaries['max'])/1200.0)) * 1200

        return_none = {
            'step': 0,
            'slices': [{
                'start': float(salaries['min']) if salaries['min'] else None,
                'end': float(salaries['max']) if salaries['max'] else None,
                'count': cohort.count(),
                'ratio': round((float(cohort_full_time.count()) / float(total_in_cohort)) * 100, 1)
            }]
        }

        diff = end - start

        if diff == 0:
            # All employees in the parent organization earn the same
            return return_none

        if cohort == parent_cohort:
            number_of_bins = decimal.Decimal(math.ceil(math.sqrt(cohort.count())))
            if number_of_bins <= 6 or parent_cohort_full_time.count() <= 10:
                number_of_bins = 6
            else:
                number_of_bins = 12
        else:
            number_of_bins = decimal.Decimal(math.ceil(math.sqrt(parent_cohort.count())))
            if number_of_bins < 1:
                return return_none
            elif diff < 20000:
                number_of_bins = 6
            elif diff < 40000 or parent_cohort_full_time.count() <= 10:
                number_of_bins = 8
            else:
                number_of_bins = 10
        step = math.floor(diff / decimal.Decimal(number_of_bins))

        slices = []
        while start < salaries['max']:
            if start == salaries['min']:
                cohort_total = (cohort_full_time.filter(compensation__gte=start,
                                              compensation__lte=start + step)
                                      .count())
            else:
                cohort_total = (cohort_full_time.filter(compensation__gt=start,
                                              compensation__lte=start + step)
                                      .count())
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
            # Employee works for a department,
            # also calculate parent organization stats
            kwargs = {
                'position__organization': obj,
            }

        else:
            kwargs = {
                'position__organization__parent': obj,
            }

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
