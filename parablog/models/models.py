import datetime
import uuid

from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Text,
    DateTime,
    ARRAY,
    ForeignKey
)

from .meta import Base


class BaseMixin(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class BlogPost(Base, BaseMixin):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    uri = Column(Unicode(127), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(ARRAY(Text))

    def __init__(self, title, **kwargs):
        uid = uuid.uuid4()
        self.uri = uid.hex
        super(BlogPost, self).__init__(**kwargs)
        self.title = title


class Comment(Base, BaseMixin):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    blogpost_id = Column(Integer, ForeignKey(BlogPost.id, onupdate='CASCADE', ondelete='CASCADE'))
    paragraph_id = Column(Integer, nullable=False)  # indicates the index number of paragraph
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text)

    def __init__(self, blogpost_id, paragraph_id, **kwargs):
        super(Comment, self).__init__(**kwargs)
        self.paragraph_id = paragraph_id
        self.blogpost_id = blogpost_id

