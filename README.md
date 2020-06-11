# Girlsky_spider

## 项目简介

一个初学者的简单练习...

利用scrapy框架实现girlsky.cn首页妹子图中所有图片下载。

利用`ImagesPipeline`实现异步图片下载。

修改下载路径，检测文件是否存在，避免重复下载：

```python
def file_path(self, request, response=None, info=None):
    # opath是原来的路径
    opath = super().file_path(request, response, info)
    image_name = opath.replace('full/', '')
    path = os.path.join(request.meta['item']['title'], image_name)
    print(path)
    if not os.path.exists(path):
        return path
```

图片下载到同路径`images`文件夹中。
