import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Floors(SqlAlchemyBase):
    __tablename__ = 'floors'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    floor = sqlalchemy.Column(sqlalchemy.String)

    rooms = orm.relationship("Rooms", back_populates='floors')