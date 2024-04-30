import enum
from typing import Optional, List

from sqlalchemy import ForeignKey, Text, BigInteger
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped

from bot.db.base import Base
from bot.db.chains import ChainType, ChainStage


class LoopEnum(enum.Enum):
    first = "1"
    second = "2"
    third = "3"
    fourth = "4"
    subscriber = "done"


class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chain_type: Mapped[Optional[ChainType]]
    chain_phase: Mapped[Optional[ChainStage]]
    username: Mapped[Optional[str]]
    packages: Mapped["Package"] = relationship(back_populates="user", lazy='selectin')
    tales: Mapped[List["Tale"]] = relationship(back_populates="user", lazy='selectin')
    subscription: Mapped["Subscription"] = relationship(back_populates="user", lazy='selectin')

    loop: Mapped[LoopEnum] = mapped_column(server_default=LoopEnum.first.name)

    def __repr__(self):
        return f'{self.tg_id=} {self.tales=}'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    tg_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), primary_key=True)
    till_end: Mapped[int]
    user: Mapped["User"] = relationship(back_populates="subscription")


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
    description_prompt: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    user: Mapped["User"] = relationship(back_populates='tales')

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
