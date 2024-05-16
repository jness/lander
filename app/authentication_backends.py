from django.conf import settings
from django.contrib.auth.backends import ModelBackend

from django_otp.plugins.otp_totp.models import TOTPDevice


class TOTPModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Custom authenticate method to check OTP
        """

        # call django base ModelBackend
        user = super().authenticate(request, username, password, **kwargs)

        # if OTP_ENABLED verify posted one time password
        if user and settings.OTP_ENABLED:
            one_time_password = int(request.POST['otp'])
            devices = TOTPDevice.objects.filter(user_id=user.id)

            for device in devices:
                if device.verify_token(one_time_password):
                    return user  # successful one time password
                
            return  # failed one time password

        return user