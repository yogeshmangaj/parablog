from __future__ import unicode_literals

import logging
import re

from parablog.models import BlogPost
from parablog.utils import SessionMixin

log = logging.getLogger(__name__)


class BlogPostService(SessionMixin):
    def __init__(self, session):
        super(BlogPostService, self).__init__(session)
        self.session = session

    def create(self, title, content):
        """
        :param title: Title of the blog post
        :type title: basestring
        :param content: Content of the post
        :type content: basestring|unicode
        :return: Blogpost object
        :rtype: BlogPost
        """
        split_content = re.split("(?<=[^\n])\n\n", content)
        return self.save(BlogPost(title, content=split_content))

    def get_by_uri(self, uri):
        """
        :rtype: BlogPost
        """
        return self.session.query(BlogPost).filter(BlogPost.uri == uri).first()

    def list(self, columns=None):
        query = self.session.query(BlogPost)
        if columns is not None:
            query = self.session.query(*columns)
        return query
