from settings.local import *


SEND_EMAILS = False

DATABASES['default']['TEST'] = {
    'NAME': 'test_test',
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
