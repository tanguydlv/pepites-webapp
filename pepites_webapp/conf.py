import os
import sys
import datetime

# Configuration
try:
    DATABASE_URL = os.environ['DATABASE_URL']
    API_URL = os.environ['API_URL'].strip('/')
    SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

    FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY', FLASK_SECRET_KEY)

    RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
    RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

    SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
    SLACK_URL = os.environ['SLACK_URL']

    REDIRECT_SCHEME = os.environ.get('REDIRECT_SCHEME', 'https')  # Used as url scheme for all redirects

# Constants
    MIN_PASSWORD_LEN = 6
    MAX_PASSWORD_LEN = 50
    MAX_LOGIN_ATTEMPTS = 3
    BAN_MAX_LOGIN_ATTEMPTS_DURATION = datetime.timedelta(minutes=5)
    ACTIVATION_CODE_LIFETIME = datetime.timedelta(hours=24)
    SENDGRID_EMAIL_FROM = 'noreply@rewardprotocol.com'
    SENDGRID_TEMPLATES = {
        'confirm_user_email': '9edef624-9721-4e58-bc89-68cbaed46339',
    }

except KeyError as ke:
    print(f'Missing mandatory configuration env variable: {ke}')
    sys.exit(1)
