from __future__ import unicode_literals

import logging

log = logging.getLogger(__name__)

POST_PREVIEW_CHAR_LENGTH = 100

MAX_PAGING_LIMIT = 50

class PAGING_LIMITS:
    POST_LIST = 5


class METHODS:
    POST = "POST"
    GET = "GET"
