# 架构说明

## TODO

- API 文档说明
- 将爬虫和 WEB 框架集成

## 文件路径

```plaintext
├── ARCHTECTURE.md  # 架构文档
├── instance        # 数据等实例文件
├── run.sh
├── script          # 数据管理脚本
└── setu_viewer
    ├── config.py   # 配置文件
    ├── __init__.py # Flask 的 create_app 函数
    ├── models      # 数据库模型
    ├── routes      # 路由
    ├── services    # 服务
    └── templates   # 模板
```

根据功能，将不同的文件分到不同文件夹中。

## 当前服务

### Pixiv 流行接口及展示

P 站接口使用了 Pixivpy 这个库进行请求和解析。

> 由于国内网络原因，所以使用了 DNS Over HTTPS 进行查询后将结果填入 `api.hosts` 中，等一个更好的方法。

### NGA 用户 wkq1w2e3 发图接口及展示

使用了爬虫进行获取 NGA 用户 wkq1w2e3 发帖中带有"谢谢茄子" Tag 的帖子内的图片链接。

### S1 用户 欧金金 发图接口及展示

使用了爬虫进行获取 S1 用户 欧金金 发帖中带有"NSFW"的帖子内的图片链接。

## 路由配置

如果为展示页面的话，则路由为`/展示站`，而 API 则是单独放在单一文件中，以`/api/版本号/接口`，返回值均为 JSON。
