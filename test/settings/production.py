from settings.staging import *


# Allowed hosts for the site
ALLOWED_HOSTS = ['test.rhizophore.com']

# Static site url, used when we need absolute url but lack request object, e.g. in email sending.
SITE_URL = 'https://test.rhizophore.com'

EMAIL_HOST_PASSWORD = 'TODO (api key)'

RAVEN_BACKEND_DSN = 'https://TODO:TODO@sentry.thorgate.eu/TODO'
RAVEN_PUBLIC_DSN = 'https://TODO@sentry.thorgate.eu/TODO'
RAVEN_CONFIG['dsn'] = RAVEN_BACKEND_DSN
