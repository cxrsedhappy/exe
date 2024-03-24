from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from db.session import Base


class User(Base, SerializerMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list[Post]] = relationship(back_populates='author')
    comments: Mapped[list[Comment]] = relationship(back_populates='author')

    def __init__(self, login, email, password):
        self.login = login
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User id={self.id}>'


class Post(Base, SerializerMixin):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped[User] = relationship(back_populates="posts")

    topic: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(default=0)

    comments: Mapped[list[Comment]] = relationship(back_populates='post', lazy='selectin')

    def __init__(self, bid):
        self.id = bid

    def __repr__(self):
        return f'<Post id={self.id} author={self.author}>'


class Comment(Base, SerializerMixin):
    __tablename__ = 'comment'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post: Mapped[Post] = relationship(back_populates='comments')
    author: Mapped[User] = relationship(back_populates='comments')

    content: Mapped[str] = mapped_column(nullable=False)
    likes: Mapped[str] = mapped_column(default=0)

    def __init__(self, cid):
        self.id = cid

    def __repr__(self):
        return f'<Comment id={self.id} blog={self.blog} likes={self.likes}>'
