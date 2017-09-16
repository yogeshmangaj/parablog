import unittest

import transaction
from pyramid import testing

from parablog.services.blogpost import BlogPostService
from parablog.services.comment import CommentService


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            # TODO: this should go in testconfig
            'sqlalchemy.url': 'postgresql+psycopg2://bloguser:bloguserpassword@localhost/testparablog'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
        )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)
        self.session.expire_on_commit = False

    def init_database(self):
        from .models.meta import Base
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestBlogpostCommentService(BaseTest):
    def setUp(self):
        super(TestBlogpostCommentService, self).setUp()
        self.init_database()
        self.bp_service = BlogPostService(self.session)
        self.comment_service = CommentService(self.session)

    def test_create_blogpost_add_comments(self):

        name = "The Zen of Python"
        content = """Beautiful is better than ugly.\n\n
        Explicit is better than implicit.\n\n
        Simple is better than complex.\n\n
        Complex is better than complicated.
        """
        post = self.bp_service.create(name, content)
        transaction.commit()
        post = self.bp_service.get_by_uri(post.uri)
        assert post.title == name
        assert len(post.content) == 4

        # add comments
        comment_content = "Readability counts"
        self.comment_service.add(post.id, 0, comment_content)
        transaction.commit()
        # fetch comments
        comments = list(self.comment_service.get_by_blogpost_id(post.id))
        assert len(comments) == 1
        assert comments[0].content == comment_content

    def test_list_blogposts(self):
        # List should be empty
        post_list = list(self.bp_service.list())
        assert len(post_list) == 0
        # add one post
        self.bp_service.create("Hello", "World")
        transaction.commit()
        post_list = list(self.bp_service.list())
        assert len(post_list) == 1
        # add another post
        self.bp_service.create("Hello2", "World2")
        transaction.commit()
        post_list = list(self.bp_service.list())
        assert len(post_list) == 2

