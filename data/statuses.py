import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Statuses(SqlAlchemyBase):
    __tablename__ = 'statuses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.String)

    applications = orm.relationship("Applications", back_populates='status')