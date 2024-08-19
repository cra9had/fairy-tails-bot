import enum
import json
from dataclasses import dataclass
from typing import Optional, List

from sqlalchemy import ForeignKey, Text, BigInteger
from sqlalchemy.orm import relationship, mapped_column, Mapped

from bot.db.base import Base


class LoopEnum(enum.Enum):
    first = "1"
    second = "2"
    third = "3"
    fourth = "4"
    subscriber = "done"


class GenderEnum(enum.Enum):
    male = "Мальчик"
    female = "Девочка"


class AgeEnum(enum.Enum):
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8

class SegmentEnum(enum.Enum):
    start = 'start'
    channel_sub = 'channel_sub'
    second_episode = 'second_episode'
    plan = 'plan'
    payed = 'payed'



class SubscriptionEnum(enum.Enum):
    trial_plan = "trial_plan"
    min_plan = 'min_plan'
    standard_plan = 'standard_plan'
    max_plan = 'max_plan'

@dataclass
class TaleParams:
    season: int = 1
    episode: int = 1
    chapter: int = 1

    def iterate(self):
        """
        Increment the chapter, and manage transitions between chapters, episodes, and seasons.
        Throws StopIteration when the end of the defined sequence is reached.
        """
        self.chapter += 1

        if self.season == 2 and self.episode == 2 and self.chapter == 5 + 1:
            raise StopIteration("End of the series reached")

        elif self.episode == 2 and self.chapter == 5 + 1:
            self.season += 1
            self.episode = 1
            self.chapter = 1

        elif self.chapter == 5 + 1:
            self.episode += 1
            self.chapter = 1

    def is_season_begin(self):
        """
        Check if the current state is the beginning of a season.
        """
        return self.chapter == 1 and self.episode == 1

    def to_json(self):
        """
        Convert the TaleParams instance to a JSON string.
        """
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        """
        Create a TaleParams instance from a JSON string.
        """
        params = json.loads(json_str)
        return TaleParams(**params)


class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]]
    chapters_available: Mapped[int] = mapped_column(server_default="1")
    packages: Mapped["Package"] = relationship(back_populates="user", lazy='selectin')
    tales: Mapped[List["Tale"]] = relationship(back_populates="user", lazy='selectin')
    subscription: Mapped["Subscription"] = relationship(back_populates="user", lazy='selectin')

    subscription_plan: Mapped[SubscriptionEnum] = mapped_column(server_default=SubscriptionEnum.trial_plan.name)

    segment: Mapped[Optional[SegmentEnum]]

    child: Mapped["Child"] = relationship(back_populates="parent", lazy="selectin")

    loop: Mapped[LoopEnum] = mapped_column(server_default=LoopEnum.first.name)

    def __repr__(self):
        return f'{self.tg_id=} {self.tales=}'


class Child(Base):
    __tablename__ = 'childs'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    name: Mapped[str]
    gender: Mapped[Optional[GenderEnum]]
    age: Mapped[Optional[AgeEnum]]
    activities: Mapped[str]

    parent_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id', ondelete='CASCADE'))

    parent: Mapped["User"] = relationship(back_populates="child")



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
