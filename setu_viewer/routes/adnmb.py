from flask import Blueprint, render_template

from setu_viewer.models.picture_url import PictureSource
from setu_viewer.services.random_img import random_img

adnmb_bp = Blueprint("adnmb", __name__)


@adnmb_bp.route("/adnmb", methods=["GET"])
def show_random_picture():
    """显示 ADNMB 来源的色图"""
    return render_template("show_picture.html",
                           url=random_img(PictureSource.ADNMB))
