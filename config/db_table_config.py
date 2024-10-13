from datetime import datetime

from sqlalchemy import BIGINT, VARCHAR, func, ForeignKey, Integer
from sqlalchemy import Float
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr
from sqlalchemy.testing.schema import mapped_column
from typing_extensions import Annotated


class Base(DeclarativeBase):
    pass


class TableNameMixin:
    # Take the Class name and use it for the table name
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


int_pk = Annotated[int,
mapped_column(Integer, primary_key=True, autoincrement=True)
]

user_fk = Annotated[int,
mapped_column(BIGINT, ForeignKey('user.user_id', ondelete='SET NULL'))
]

str_2000 = Annotated[str, mapped_column(VARCHAR(2000))]


class CreateUpdateMixin:
    creation_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    update_date: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[user_fk]
    updated_by: Mapped[user_fk]


class User(Base, TableNameMixin, CreateUpdateMixin):
    user_id: Mapped[int_pk]
    first_name: Mapped[str_2000]
    last_name: Mapped[str_2000]
    disabled: Mapped[str] = mapped_column(VARCHAR(1), server_default='N')


class Activity(Base, TableNameMixin, CreateUpdateMixin):
    activity_id: Mapped[int_pk]
    activity_desc: Mapped[str_2000]
    disabled: Mapped[str] = mapped_column(VARCHAR(1), server_default='N')

    def to_dict(self):
        return {
            'activity_id': self.activity_id,
            'activity_desc': self.activity_desc
        }


class Workout(Base, TableNameMixin, CreateUpdateMixin):
    workout_id: Mapped[int_pk]
    activity_id: Mapped[int] = mapped_column(Integer, ForeignKey('activity.activity_id'))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.user_id'))
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False)
    end_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'workout_id': self.workout_id,
            'activity_id': self.activity_id,
            'user_id': self.user_id,
            'start_time': self.start_time,
            'end_time': self.end_time
        }


class WorkoutDetail(Base, TableNameMixin, CreateUpdateMixin):
    workout_detail_id: Mapped[int_pk]
    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey('workout.workout_id', ondelete='CASCADE'))
    rep_count: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    start_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True)
    end_time: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'workout_detail_id': self.workout_detail_id,
            'workout_id': self.workout_id,
            'rep_count': self.rep_count,
            'weight': self.weight,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
