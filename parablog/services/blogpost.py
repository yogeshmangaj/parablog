from __future__ import unicode_literals

import logging
import re

from parablog.const import PAGING_LIMITS, MAX_PAGING_LIMIT
from parablog.models import BlogPost
from parablog.utils import SessionMixin

log = logging.getLogger(__name__)


class BlogPostService(SessionMixin):
    def __init__(self, session):
        super(BlogPostService, self).__init__(session)
        self.session = session

    def create(self, title, content):
        """
        Creates a new Blog Post. The content is a single string, that will be broken down into paragraphs and
        stored as individual paragraphs in an array.

        The index of each paragraph (denoted as `paragraph_id`) will be used to store comments against it.
        The following operations for paragraphs (although not supported as of v0.1) will be handled as described,
        - Edition or deletion will not remove the paragraph but instead set the value to None so as to maintain
        the consistency of the Paragraph IDs.
        - Reordering or inserting paragraphs will updated the `paragraph_id` for the corresponding `Comment` instances.

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
        Get BlogPost by URI
        :param uri: URI of blog post
        :type uri: basestring
        :return: Blogpost object
        :rtype: BlogPost
        """
        return self.session.query(BlogPost).filter(BlogPost.uri == uri).first()

    def list(self, columns=None, offset=0, limit=PAGING_LIMITS.POST_LIST):
        """
        Return a sqlalchemy query iterator that yields complete instances of `BlogPost` if `columns` is not specified
        or objects with specified attributes in `columns`.

        `offset` and `limit` will specify the range of objects to be fetched

        :param columns: (optional) List of sqlalchemy column definitions that should be fetched
        :type columns: list
        :param offset: Number of rows to skip from the start
        :type offset: int
        :param limit: Number of rows that will be a part of the list that will be returned, has an upper bound as
            defined by `const.MAX_PAGING_LIMIT`
        :type limit: int
        :return: Sqlalchemy query result collection
        """
        query = self.session.query(BlogPost)
        if columns is not None:
            query = self.session.query(*columns)
        offset = max(offset, 0)
        limit = min(limit, MAX_PAGING_LIMIT)
        return query.limit(limit).offset(offset)

    def count(self):
        """
        Return count of blog posts
        :rtype: int
        """
        return self.session.query(BlogPost).count()