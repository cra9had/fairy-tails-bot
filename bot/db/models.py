from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped

from bot.db.base import Base


class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[Optional[str]]
    packages: Mapped["Package"] = relationship(back_populates="user")
    tales: Mapped["Tale"] = relationship(back_populates="user")
    subscription: Mapped["Subscription"] = relationship(back_populates="user")

    def __repr__(self):
        return f'{self.tg_id=} {self.tales=}'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), primary_key=True)
    till_end: Mapped[int]
    user: Mapped["user"] = relationship(back_populates="subscription")


class Package(Base):
    __tablename__ = 'packages'
    id: Mapped[int] = mapped_column(primary_key=True)
    tales_quantity: Mapped[int]
    price: Mapped[float]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    user: Mapped["User"] = relationship(back_populates='packages')

    def __repr__(self):
        return f'{self.price=} {self.tales_quantity=} {self.user_id=}'


class Tale(Base):
    __tablename__ = 'tales'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    seasons: Mapped["Season"] = relationship(back_populates='tale')

    def __repr__(self):
        return f'{self.title=} {self.seasons=}'


class Season(Base):
    __tablename__ = 'seasons'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    tale_id: Mapped[int] = mapped_column(ForeignKey("tales.id"))

    tale: Mapped["Tale"] = relationship(back_populates="seasons")
    episodes: Mapped["Episode"] = relationship(back_populates="season")

    def __repr__(self):
        return f'{self.title=} {self.episodes=}'


class Episode(Base):
    __tablename__ = 'episodes'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[Optional[str]]
    season_id: Mapped[int] = mapped_column(ForeignKey('seasons.id'))
    season: Mapped["Season"] = relationship(back_populates="episodes")
    chapters: Mapped["Chapter"] = relationship(back_populates="episode")

    def __repr__(self):
        return f'{self.title=} {self.chapters=}'


class Chapter(Base):
    __tablename__ = 'chapters'
    id: Mapped[int] = mapped_column(primary_key=True)
    episode_id: Mapped[int] = mapped_column(ForeignKey('episodes.id'))
    text_chapter: Mapped[str]
    audio_chapter: Mapped[Optional[str]]

    episode: Mapped["Episode"] = relationship(back_populates="chapters")

    def __repr__(self):
        return f'{self.id=} {self.text_chapter=} {self.audio_chapter=}'
