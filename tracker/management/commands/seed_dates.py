from django.core.management.base import BaseCommand
from tracker.models import Date
import datetime


class Command(BaseCommand):
    help = "Populate Date dimension with all days from 2020 to 2030"

    def handle(self, *args, **kwargs):
        start = datetime.date(2020, 1, 1)
        end = datetime.date(2030, 12, 31)
        delta = datetime.timedelta(days=1)

        created_count = 0
        current = start
        while current <= end:
            obj, created = Date.objects.get_or_create(
                full_date=current,
                defaults={
                    "year": current.year,
                    "month": current.month,
                    "day": current.day,
                    "weekday": current.strftime("%A"),
                    "quarter": (current.month - 1) // 3 + 1,
                },
            )
            if created:
                created_count += 1
            current += delta

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Date dimension populated. {created_count} new rows added."
            )
        )
