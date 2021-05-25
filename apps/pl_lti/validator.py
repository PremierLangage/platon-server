import logging

from pylti.common import verify_request_common
from rest_framework.request import Request

logger = logging.getLogger(__name__)


def is_valid_request(consumer_key: str, consumer_secret: str, request: Request):
    consumers = {
        consumer_key: {
            "secret": consumer_secret,
        }
    }

    try:
        return verify_request_common(
            consumers,
            request.build_absolute_uri(),
            request.method,
            request.META,
            request.POST.dict()
        )
    except Exception as e:
        logger.error(e)
        return False
