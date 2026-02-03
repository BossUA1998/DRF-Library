from django.core.management.base import BaseCommand
from django_q.models import Schedule
from django_q.tasks import schedule


class Command(BaseCommand):
    help = "Setting up periodic tasks"

    def handle(self, *args, **options):
        task_func = "user.management.commands.run_bot.notification_for_telegram_ids"

        if Schedule.objects.filter(func=task_func).exists():
            self.stdout.write(
                self.style.WARNING(f"The task {task_func} already exists. Skipping.")
            )
        else:
            schedule(func=task_func, schedule_type="C", cron="00 12 * * *", repeats=-1)
            self.stdout.write(
                self.style.SUCCESS(f"Task {task_func} successfully created!")
            )
