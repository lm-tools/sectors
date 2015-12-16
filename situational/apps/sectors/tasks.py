from django.conf import settings

from celery.utils.log import get_task_logger
from redlock import Redlock

logger = get_task_logger(__name__)
population_timeout = settings.REPORT_POPULATION_TIMEOUT
dlm = Redlock([settings.REDIS_URL])  # Distibuted Lock Manager
