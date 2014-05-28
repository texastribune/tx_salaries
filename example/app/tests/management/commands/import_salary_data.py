from django.test import TestCase

from tx_salaries.models import OrganizationStats, PositionStats
from tx_people.models import Organization, Post


class StatsForAll(TestCase):
    def test_stats_for_all_organizations(self):
        self.assertEqual(Organization.objects.count(),
                         OrganizationStats.objects.count())

    def test_stats_for_all_positions(self):
        self.assertEqual(Post.objects.count(), PositionStats.objects.count())
