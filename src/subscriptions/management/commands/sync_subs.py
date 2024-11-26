from django.core.management .base import BaseCommand

from subscriptions.models import Subscription

class Command(BaseCommand):
    def handle(self, *args, **options):
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(perms)