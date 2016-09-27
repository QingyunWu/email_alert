import os
__author__ = 'Qingyun Wu'

# hide key in environment variables

# URL = "https://api.mailgun.net/v3/sandbox99ea708e421348deae802e401298d8ea.mailgun.org/messages"
URL = os.environ.get('MAILGUN_URL')
# API_KEY = "key-f09f492eaede684f145a2fda9e151f6f"
API_KEY = os.environ.get('MAILGUN_KEY')

# FROM = "postmaster@sandbox99ea708e421348deae802e401298d8ea.mailgun.org"
FROM = os.environ.get('MAILGUN_FROM')

ALERT_TIMEOUT = 10
COLLECTION = "alerts"