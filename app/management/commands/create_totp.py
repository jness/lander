import io
import sys

import qrcode
from django.conf import settings
from django_otp.plugins.otp_totp.models import TOTPDevice

from . import ScheduledCommand
from app.models import Schedule


class Command(ScheduledCommand):
    help = "Create a TOTP device for user_id"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int)

    def handle(self, *args, **options):

        if not settings.OTP_ENABLED:
            msg = 'Time-based one-time is disable, check OTP_ENABLED in settings.'
            self.log(msg, error=True)
            self.report_failure()
            sys.exit(1)

        # wrap entire logic in try in order to log
        # to our django models
        try:
            # create and save new totp object
            user_id = options["user_id"]
            device = TOTPDevice(user_id=user_id, name="Authenticator")
            device.save()
            # display QR code in terminal
            qr = qrcode.QRCode()
            qr.add_data(device.config_url)
            f = io.StringIO()
            qr.print_ascii(out=f)
            f.seek(0)
            print(f.read())
        except Exception as e:
            self.log(e, error=True)
            self.report_failure()
            sys.exit(1)

        self.stdout.write(
            self.style.SUCCESS('Successfully created TOTP device for user_id "%s"' % user_id)
        )

        # log message to ScheduleLog is executed via schedule
        self.log('Successfully created TOTP device for user_id "%s"' % user_id)
        self.report_success()
