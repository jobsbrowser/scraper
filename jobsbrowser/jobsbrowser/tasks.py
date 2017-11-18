from celery import Celery
from celery.utils.log import get_task_logger
from scrapy.conf import settings

app = Celery('jobsbrowser.tasks', broker=settings["CELERY_BROKER"])

logger = get_task_logger(__name__)


@app.task
def send_offer(offer):
    logger.info(f"Received offer {offer['offer_id']}")
