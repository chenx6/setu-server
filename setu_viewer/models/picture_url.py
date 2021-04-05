# type: ignore
from enum import Enum

from .base import db


class PictureSource(Enum):
    NGA = 1
    Stage1st = 2
    ADNMB = 3


class PictureUrl(db.Model):
    """
    `id` id
    `source` 来源，请查看 `PictureSource` 类定义
    `url` 图片链接
    """
    __tablename__ = "picture_url"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer)
    url = db.Column(db.Text, unique=True)
