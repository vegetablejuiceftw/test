from test.celery import app as celery_app


default_app_config = 'test.apps.TestConfig'

__all__ = ['celery_app']
