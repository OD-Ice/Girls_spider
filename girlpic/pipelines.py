# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from girlpic.settings import IMAGES_STORE

# 使用ImagesPipeline这个就不运行了
class GirlpicPipeline:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def process_item(self, item, spider):
        title = item['title']
        urls = item['image_urls']
        title_path = os.path.join(self.path, title)
        if not os.path.exists(title_path):
            os.mkdir(title_path)

        image_name = os.path.join(title_path, urls.split('/')[-1])
        request.urlretrieve(urls, image_name)
        return item

# 更改存储路径需要重新定义ImagesPipeline
class GirlsImagesPipeline(ImagesPipeline):
    # 这个方法是发送下载请求之前调用，其实就是发送下载请求的
    def get_media_requests(self, item, info):
        # request_objs = super().get_media_requests(item, info)
        # # 第一种方法 把item绑定到这里，便于file_path程序使用
        # for request_obj in request_objs:
        #     request_obj.item = item
        # return request_objs

        # 第二种方法 用meta参数进行传递
        return [Request(x, meta={'item': item}) for x in item.get(self.images_urls_field, [])]

    # 这个方法是在存储文件时调用的，来获取图片的存储路径
    def file_path(self, request, response=None, info=None):
        # opath是原来的路径
        opath = super().file_path(request, response, info)
        image_name = opath.replace('full/', '')
        path = os.path.join(request.meta['item']['title'], image_name)
        print(path)
        if not os.path.exists(path):
            return path
