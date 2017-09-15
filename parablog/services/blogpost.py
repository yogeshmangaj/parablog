from __future__ import unicode_literals

import logging
import re

import transaction

from parablog.models import BlogPost, Comment

log = logging.getLogger(__name__)


class BlogPostService(object):
    def __init__(self, session):
        self.session = session

    def create(self, title, content):
        split_content = re.split("(?<=[^\n])\n\n", content)
        blog_post = BlogPost(title, content=split_content)
        self.session.add(blog_post)
        transaction.commit()
        return blog_post

    def get_by_uri(self, uri):
        return self.session.query(BlogPost).filter(BlogPost.uri == uri).first()


class CommentService(object):
    def __init__(self, session):
        self.session = session

    def add(self, blogpost_id, paragraph_id, content):
        comment = Comment(blogpost_id, paragraph_id, content=content)
        self.session.add(comment)
        return comment
