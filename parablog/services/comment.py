from __future__ import unicode_literals

import logging

from parablog.models import Comment

log = logging.getLogger(__name__)


class CommentService(object):
    def __init__(self, session):
        self.session = session

    def add(self, blogpost_id, paragraph_id, content):
        comment = Comment(blogpost_id, paragraph_id, content=content)
        self.session.add(comment)
        return comment

    def get_by_blogpost_id(self, blogpost_id, order_by=None):
        if order_by is None:
            order_by = Comment.updated_at
        return self.session.query(Comment).filter(Comment.blogpost_id == blogpost_id)\
            .order_by(order_by).all()