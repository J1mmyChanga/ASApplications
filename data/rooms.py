import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Rooms(SqlAlchemyBase):
    __tablename__ = 'rooms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    floor_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("floors.id"))
    room = sqlalchemy.Column(sqlalchemy.String)

    floors = orm.relationship("Floors", back_populates='rooms')
    applications = orm.relationship("Applications", back_populates='room')