from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        [OrganizationStats.objects.denormalize(o) for o in Organization.objects.all()]
        [PositionStats.objects.denormalize(p) for p in Post.objects.all()]
