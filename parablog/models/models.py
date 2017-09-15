import datetime
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


class BlogPost(Base):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    uri = Column(Unicode(127), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(ARRAY(Text))


class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    blogpost_id = Column(Integer, ForeignKey(BlogPost.id, onupdate='CASCADE', ondelete='CASCADE'))
    paragraph_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text)

