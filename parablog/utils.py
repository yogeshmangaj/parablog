from __future__ import unicode_literals

import logging

import transaction

log = logging.getLogger(__name__)


def alchemy_result_to_dict(res):
    res_dict = dict()
    for field in res._fields:
        res_dict[field] = getattr(res, field)
    return res_dict


class SessionMixin(object):
    def __init__(self, session):
        self.session = session

    def save(self, obj):
        self.session.add(obj)
        transaction.commit()
        return self.session.merge(obj)