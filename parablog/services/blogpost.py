from __future__ import unicode_literals

import logging
import re

import transaction

from parablog.models import BlogPost

log = logging.getLogger(__name__)


class BlogPostService(object):
    def __init__(self, session):
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
        blog_post = BlogPost(title, content=split_content)
        self.session.add(blog_post)
        transaction.commit()
        return blog_post

    def get_by_uri(self, uri):
        """
        :rtype: BlogPost
        """
        return self.session.query(BlogPost).filter(BlogPost.uri == uri).first()

    def list(self):
        return self.session.query(BlogPost).all()
