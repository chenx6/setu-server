"""
请注意，尽量减少使用这个爬虫，因为对服务器压力大...
"""
from re import compile
from typing import NamedTuple
from time import sleep
from json import dumps, loads
from functools import reduce
from logging import getLogger

from bs4 import BeautifulSoup
from requests import Session

logger = getLogger("s1-spider")


class PostListItem(NamedTuple):
    url: str
    title: str


class Stage1stSpider:
    host = "https://bbs.saraba1st.com/2b/"

    def __init__(self) -> None:
        self.s = Session()
        with open("cookie.json") as f:
            self.s.cookies.update(loads(f.read()))

    def session(self):
        return self.s

    @staticmethod
    def post_list(text: str) -> list[PostListItem]:
        """获取发帖列表"""
        soup = BeautifulSoup(text, features="html.parser")
        posts_raw = soup.find_all("a", href=compile("thread-.+"))
        ret: list[PostListItem] = []
        for i in posts_raw:
            if i.text.isnumeric():
                continue
            ret.append(PostListItem(i['href'], i.text))
        return ret

    @staticmethod
    def post_pic(text: str):
        """获取帖子中的链接"""
        soup = BeautifulSoup(text, features="html.parser")
        img_addr_list: list[str] = []
        try:
            # 找到所有回复
            reply_html_list = soup.find_all('table', class_='plhin')
            first_reply = reply_html_list[0]
            # 找到回复内容
            reply_text = first_reply.find(class_='t_f')
            # 提取 img 标签中 file 属性
            imgs = reply_text.find_all('img')
            for img in imgs:
                if 'file' in img.attrs.keys():
                    img_addr_list.append(img['file'])
        except Exception as e:
            print(e)
        return img_addr_list

    def all_posts(self,
                  home_url: str,
                  sleep_sec: float = 0.3) -> list[PostListItem]:
        count = 1
        ret = []
        while True:
            home_response = self.s.get(home_url, params={"page": count})
            lst = Stage1stSpider.post_list(home_response.text)
            if len(lst) == 0:
                break
            ret += lst
            sleep(sleep_sec)
            count += 1
        return ret


def main():
    spider = Stage1stSpider()
    s = spider.session()
    post_list = spider.all_posts(
        "https://bbs.saraba1st.com/2b/home.php?mod=space&uid=461722&do=thread&view=me&order=dateline&from=space"
    )
    logger.info(f"[*] len(post_list) = {len(post_list)}")
    post_iter = filter(lambda x: 'NSFW' in x.title, post_list)
    post_contents = map(s.get, (f'https://bbs.saraba1st.com/2b/{i.url}'
                                for i in post_iter))
    img_urls = reduce(
        lambda x, y: x + y,
        map(Stage1stSpider.post_pic, (i.text for i in post_contents)))
    logger.info(f"[*] len(img_urls) = {len(img_urls)}")
    # TODO: 使用 flask-sqlalchemy
    with open("instance/s1_pictures.json", 'w') as f:
        f.write(dumps(img_urls))
