from typing import Any
from pixivpy3 import ByPassSniApi

api = ByPassSniApi()
# api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
api.hosts = "https://210.140.131.201"  # TODO: CF DOH is broken, manual set hosts
api.auth(refresh_token='uXooTT7xz9v4mflnZqJUO7po9W5ciouhKrIDnI2Dv3c')


def popular_preview(word: str) -> Any:
    """P 站热度搜索预览"""
    params = {
        "filter": "for_android",
        "include_translated_tag_results": "true",
        "merge_plain_keyword_results": "true",
        "word": word,
        "search_target": "exact_match_for_tags"
    }
    raw_result = api.no_auth_requests_call(
        'GET', f'{api.hosts}/v1/search/popular-preview/illust', params=params)
    return raw_result.json()