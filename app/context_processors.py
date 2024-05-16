from django.conf import settings


def otp_enabled(context):
  """
  Add OTP_ENABLED on every template
  """
  return {'OTP_ENABLED': settings.OTP_ENABLED}


def site_id(context):
  """
  Add SITE_ID on every template
  """
  return {'SITE_ID': settings.SITE_ID}
