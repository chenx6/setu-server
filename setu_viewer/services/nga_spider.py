"""
请注意，尽量减少使用这个爬虫，因为对服务器压力大...
"""
from time import sleep
from re import compile
from random import randint
from typing import Any, NamedTuple
from logging import getLogger
from functools import reduce
from json import dumps

from requests import Session
from bs4 import BeautifulSoup
from arrow import get

logger = getLogger("nga-spider")


class PostListContent(NamedTuple):
    node: Any
    post_date: str


class NGASpider:
    """
    辅助爬虫类
    """

    guest_js_regex = compile(r"guestJs=(\d+);")
    img_inner_regex = compile(r"\[img\]([\w0-9/\-.]+)\[\/img\]")
    picture_base_regex = compile(r"__ATTACH_BASE_VIEW_SEC = '(.+)',")
    host = "https://bbs.nga.cn"
    search_url = "https://bbs.nga.cn/thread.php?key={}"
    s = Session()

    def __init__(self) -> None:
        self.s.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"

    def session(self) -> Session:
        return self.s

    @staticmethod
    def author_post_list(text: str) -> list[PostListContent]:
        """提取出发帖列表"""
        soup = BeautifulSoup(text, features="html.parser")
        topic_rows = soup.find_all(class_="topicrow")
        return list(
            map(
                lambda x: PostListContent(
                    x.find_next("a", class_="topic"),
                    x.find_next(class_="postdate").text,
                ),
                topic_rows,
            ))

    @staticmethod
    def get_post_page_count(text: str) -> int:
        post_count_regex = compile(
            r"var __PAGE = \{0:'.+',1:(\d+),2:\d+,3:\d+\};")
        return int(post_count_regex.search(text).group(1))

    def bypass_guest(self, sleep_time: int):
        """绕过“访客不能直接访问”"""
        # 进行第一次请求后，大概率是会被“访客不能直接访问”拦住，所以提取出发帖列表，获取相关信息
        topic_url = f"{self.host}/read.php?tid=26136121"
        response = self.s.get(topic_url)
        response_text = response.content.decode("gbk")
        # 提取出页面中的 guestJs 变量加入 Cookie
        guest_js, *_ = self.guest_js_regex.findall(response_text)
        self.s.cookies.set("guestJs", guest_js)
        # 注意，可能是反爬虫措施，得 sleep 一下才能继续
        sleep(sleep_time)

    def get_post_pictures(self, read_url: str) -> list[str]:
        """获取帖子中图片的 URL"""
        read_response = self.s.get(read_url)
        read_text = read_response.content.decode("gbk", errors="ignore")
        # 获取图片基础网址，顶楼内容
        picture_base, *_ = self.picture_base_regex.findall(read_text)
        soup = BeautifulSoup(read_text, features="html.parser")
        post_raw = soup.find("p", id="postcontent0")
        # 解析数据
        return list(
            map(
                lambda x: f"https://{picture_base}/attachments{x[1:]}",
                self.img_inner_regex.findall(post_raw.text),
            ))


def add(x1, x2):
    return x1 + x2


def get_data(spider: NGASpider, url: str, page: int) -> list[PostListContent]:
    """获取所有发帖"""
    s = spider.session()
    ret = []
    for i in range(2, page + 1):
        real_response = s.get(f"{url}&page={page}")
        ret += NGASpider.author_post_list(real_response.content.decode("gbk"))
    return ret


def wash_data(spider: NGASpider, posts: list, update: bool) -> list:
    """清洗数据"""
    eggplants = filter(lambda x: "[谢谢茄子]" in x.node.text \
        and "帖子发布或回复时间超过限制" not in x.node.text,
        posts)
    if update:
        with open("data/last_update.txt", "r") as f:
            last_update = get(float(f.read()), tzinfo="CST")
        if not last_update:
            last_update = get(0)
        eggplants = filter(
            lambda x: get(int(x.post_date), tzinfo="CST") > last_update,
            eggplants)
    eggplants = map(lambda x: x.node["href"], eggplants)
    return reduce(
        add,
        map(lambda x: spider.get_post_pictures(f"{spider.host}{x}"),
            eggplants),
    )


def main(update: bool = False, json_data: bool = False):
    """主函数，主要逻辑处理"""
    # 获取发帖人第一页发帖列表
    spider = NGASpider()
    spider.bypass_guest(1)
    s = spider.session()
    real_response = s.get(f"{spider.host}/thread.php?authorid=24278093",
                          params={"rand": randint(0, 100)})
    logger.info(f"Status code: {real_response.status_code}")
    real_text = real_response.content.decode("gbk")
    # 获取发帖页数，以获取所有页数
    post_page_count = NGASpider.get_post_page_count(real_text)
    posts = get_data(spider, f"{spider.host}/thread.php?authorid=24278093",
                     post_page_count)
    # 根据条件清洗数据
    result = wash_data(spider, posts, update)
    logger.info(f"Data len: {len(result)}")
    # 存数据
    if json_data:
        with open("instance/nga_picture.json", "w") as f:
            f.write(dumps(result))
    """
    TODO: 使用 flask-sqlalchemy 进行数据存储
    with DbHelper("./data/url.db", not update) as helper:
        for d in result:
            helper.insert(d)
    """
    with open("instance/nga_last_update.txt", "w") as f:
        f.write(str(get().timestamp()))
    logger.info("Finished!")


if __name__ == "__main__":
    main()
