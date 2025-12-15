import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Applications(SqlAlchemyBase):
    __tablename__ = 'applications'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("statuses.id"), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    finished_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    phoneNumber = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    room_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    notify = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)

    status = orm.relationship("Statuses", back_populates='applications')
    room = orm.relationship("Rooms", back_populates='applications')
    photos = orm.relationship("Photos", back_populates='application')