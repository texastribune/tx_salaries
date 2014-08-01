from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        '''
        Denormalize statistics for all current Organizations and Positions
        '''
        [OrganizationStats.objects.denormalize(o) for o in Organization.objects.all()]
        [PositionStats.objects.denormalize(p) for p in Post.objects.all()]
