# 自助色图 API (WIP)

无人工干预，自动从各种渠道获取色图，并通过 API 等方式进行色图的重新分发

# 功能

## 查看色图

|路由|参数|功能|
|-|-|-|
|`/stage1st`||显示 S1 用户欧金金发的色图|
|`/nga`||显示 NGA 用户 wkq1w2e3 发的色图|
|`/adnmb`||显示 ADNMB 中 JP 图片|

## 搜索色图

|路由|参数|功能|
|-|-|-|
|`/pixiv/popular`|word|搜索"word"这个tag的热度排行|

## 使用色图(?)

|路由|参数|返回|
|-|-|-|
|`/api/v1/stage1st`||带 URL 的 JSON|
|`/api/v1/nga`||带 URL 的 JSON|
|`/api/v1/adnmb`||带 URL 的 JSON|
|`/api/v1/pixiv/popular`|word|API 返回结果|

# 架构

请参考 [ARCHITECTURE.md](./ARCHITECTURE.md)

# 运行

```bash
# 请先安装好 venv 和 pip
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
# 使用 gunicorn 运行
gunicorn -w $(nproc) -b 0.0.0.0:8848 'setu_viewer:create_app()'
```
