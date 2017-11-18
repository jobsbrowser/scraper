import requests

from celery import Celery
from celery.utils.log import get_task_logger
from requests.exceptions import ConnectionError
from scrapy.conf import settings

app = Celery('jobsbrowser.tasks', broker=settings["CELERY_BROKER"])

logger = get_task_logger(__name__)


@app.task
def send_offer(offer):
    logger.info(f"Received offer {offer['offer_id']}")
    try:
        r = requests.post(settings["STORAGE_SERVICE_URL"], data=offer)
    except ConnectionError:
        logger.info(
            f"Sending offer {offer['offer_id']} failed. "
            "Service storage is unavailable."
        )
    else:
        logger.info(
            f"Offer {offer['offer_id']} sent to storage service. "
            f"Returned Code: {r.status_code}"
        )
