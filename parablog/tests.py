import unittest

import transaction
from pyramid import testing

from parablog.services.blogpost import BlogPostService


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


class TestBlogpostService(BaseTest):
    def setUp(self):
        super(TestBlogpostService, self).setUp()
        self.init_database()

    def test_create_blogpost(self):
        service = BlogPostService(self.session)
        name = "The Zen of Python"
        content = """Beautiful is better than ugly.\n\n
        Explicit is better than implicit.\n\n
        Simple is better than complex.\n\n
        Complex is better than complicated.
        """
        post = service.create(name, content)
        transaction.commit()
        post = service.get_by_uri(post.uri)
        transaction.commit()
        assert post.title == name
        assert len(post.content) == 4
