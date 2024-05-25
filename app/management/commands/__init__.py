import os
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand

from app.models import Schedule, ScheduleLog


class ScheduledCommand(BaseCommand):
    help = "Generic BaseCommand with Schedule support"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger('django.management.commands')

    def get_schedule(self):
        """
        Gets Schedule using env
        """

        if os.getenv('SCHEDULE_ID'):
            return Schedule.objects.get(id=os.getenv('SCHEDULE_ID'))
        
    def log(self, message, error=False):
        """
        Logs to ScheduleLog
        """

        if error:
            self.logger.error(message)
            message = 'ERROR: ' + str(message)
        else:
            self.logger.info(message)
            message = 'INFO: ' + str(message)

        if self.get_schedule():
            scheduled_log = ScheduleLog(schedule=self.get_schedule(), content=message)
            scheduled_log.save()
    
    def report_failure(self):
        """
        Sets last_failure_at on Schedule
        """

        if self.get_schedule():
           schedule = self.get_schedule()
           schedule.last_failure_at = timezone.localtime()
           schedule.save()

    def report_success(self):
        """
        Sets last_success_at on Schedule
        """

        if self.get_schedule():
           schedule = self.get_schedule()
           schedule.last_success_at = timezone.localtime()
           schedule.save()
