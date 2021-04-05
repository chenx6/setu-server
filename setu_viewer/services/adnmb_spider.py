"""
请注意，尽量减少使用这个爬虫，因为对服务器压力大...
"""
from typing import Any
from json import dumps
from functools import reduce

from requests import Session

s = Session()
s.headers["User-Agent"] = "HavfunClient-adnmb"
s.cookies.update(
    {"userhash": "0%10%1F6i80S%94%BA%9DL%9C%26%15%A0%F3L%C4%01%5Cb%9E%17"})
cdn = 'https://nmbimg.fastmirror.org'
blacklist_words = ['猫', '狗', '鸟', '呢']


def search(word: str, page_no: int = 1) -> Any:
    query_url = "https://adnmb3.com/Api/search?appid=nimingban"
    response = s.get(query_url, params={"q": word, "pageNo": page_no})
    return response.json()


def has_blacklist_word(needles: list[str], haystack: str) -> bool:
    return True in map(lambda x: x in haystack, needles)


def get_img(result: Any) -> list[str]:
    hits = result['hits']['hits']
    hits_iter = filter(
        lambda x: not has_blacklist_word(
            blacklist_words, x['_source']['content']),
        hits)
    hits_iter = filter(lambda x: 'img' in x['_source'].keys(), hits_iter)
    return list(
        map(
            lambda x:
            f"{cdn}/image/{x['_source']['img']}{x['_source']['ext']}",
            hits_iter))


if __name__ == "__main__":
    imgs = reduce(lambda a, b: a + b,
                  (get_img(search("jp", i)) for i in range(1, 10 + 1)))
    with open("instance/adnmb.json", 'w') as f:
        f.write(dumps(imgs))
