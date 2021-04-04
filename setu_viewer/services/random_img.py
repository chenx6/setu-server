from sqlalchemy.sql.expression import func

from setu_viewer.models.picture_url import PictureUrl, PictureSource


def random_img(source: PictureSource) -> str:
    res = PictureUrl.query.filter_by(source=source.value).order_by(
        func.random()).limit(1).one()
    return res.url
