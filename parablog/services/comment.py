from __future__ import unicode_literals

import logging

from parablog.models import Comment
from parablog.utils import SessionMixin

log = logging.getLogger(__name__)


class CommentService(SessionMixin):
    def __init__(self, session):
        self.session = session
        super(CommentService, self).__init__(session)

    def add(self, blogpost_id, paragraph_id, content):
        """
        Add a comment against a paragraph in a blog post.

        :param blogpost_id: ID (not to be confused with URI) of the blogpost
        :type blogpost_id: int
        :param paragraph_id: Index of the paragraph in the blog post
        :type paragraph_id: int
        :param content: Body of the comment
        :type content: basestring | unicode
        :return: Newly created Comment instance
        :rtype: Comment
        """
        return self.save(Comment(blogpost_id, paragraph_id, content=content))

    def get_by_blogpost_id(self, blogpost_id, order_by=None):
        """
        Gets all the comments in a blog post

        :param blogpost_id: ID (not to be confused with URI) of the blogpost
        :type blogpost_id: int
        :param order_by: Column that defines the sort, defaults to `updated_at`
        :type order_by: basestring | sqlalchemy.Column
        :return: Sqlalchemy query result iterator
        """
        if order_by is None:
            order_by = Comment.updated_at
        return self.session.query(Comment).filter(Comment.blogpost_id == blogpost_id)\
            .order_by(order_by)