from flask import Blueprint, render_template

from setu_viewer.models.picture_url import PictureSource
from setu_viewer.services.random_img import random_img

s1_bp = Blueprint("stage1st", __name__)


@s1_bp.route("/stage1st", methods=["GET"])
def show_random_picture():
    return render_template("show_picture.html",
                           url=random_img(PictureSource.Stage1st))
