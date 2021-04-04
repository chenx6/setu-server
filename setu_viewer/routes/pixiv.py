from flask import Blueprint, request, render_template

from setu_viewer.services.pixiv_popular import popular_preview

pixiv_bp = Blueprint("pixiv", __name__, url_prefix='/pixiv')


@pixiv_bp.route("/popular", methods=["GET"])
def popular_rank():
    """显示 P 站热度搜索预览结果"""
    word = request.args["word"]
    if not word:
        return render_template("error.html", message="缺少 word 参数")
    result = popular_preview(word)
    if "error" in result.keys():
        return render_template("error.html", message="word 参数错误," + result["error"])
    # URL 替换为 pixiv.cat 的链接，绕过 P 站限制
    urls = []
    for i in result['illusts'][:3]:
        urls.append(f"https://pixiv.cat/{i['id']}.jpg")
    return render_template("show_pixiv_popular.html", word=word, urls=urls)
