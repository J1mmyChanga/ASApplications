import sqlalchemy
from sqlalchemy import orm
from datetime import datetime

from .db_session import SqlAlchemyBase


class Photos(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    application_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('applications.id'), nullable=False)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Оригинальное имя
    filepath = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # Путь на сервере
    thumbnail_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)            # Путь к миниатюре
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now, nullable=False)
    order = sqlalchemy.Column(sqlalchemy.Integer, default=0, nullable=False)              # Порядок отображения

    application = orm.relationship("Applications", back_populates='photos')