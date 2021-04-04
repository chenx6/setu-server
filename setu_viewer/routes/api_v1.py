from flask import Blueprint, request

from setu_viewer.models.picture_url import PictureSource
from setu_viewer.services.random_img import random_img
from setu_viewer.services.pixiv_popular import popular_preview

api_bp = Blueprint("api", __name__, url_prefix='/api/v1')


@api_bp.route("/nga", methods=["GET"])
def nga_random_picture():
    """NGA 随机色图接口"""
    return {"url": random_img(PictureSource.NGA)}


@api_bp.route("/pixiv/popular", methods=["GET"])
def popular_prev():
    """P 站热度搜索预览接口"""
    word = request.args["word"]
    if not word:
        return {"error": "Missing word"}, 400
    result = popular_preview(word)
    return result, 200


@api_bp.route("/stage1st", methods=["GET"])
def s1_random_picture():
    """S1 随机色图接口"""
    return {"url": random_img(PictureSource.Stage1st)}
