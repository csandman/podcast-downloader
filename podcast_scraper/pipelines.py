# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import eyed3
from slugify import slugify
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.files import FilesPipeline
from scrapy import Request
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from urllib.parse import urlparse


class PodcastScraperPipeline(object):
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        self.file = open(f'{spider.name}_output.json', 'wb')
        self.exporter = JsonItemExporter(self.file, indent=2)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()


class PodcastFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item.get('file_urls'):
            for file_url in item.get('file_urls'):
                yield Request(
                    file_url,
                    meta={
                        'podcast_name': item.get('podcast_name'),
                        'title': item.get('title')
                    }
                )

    def file_path(self, request, response=None, info=None):
        podcast_name = request.meta['podcast_name']
        title = request.meta['title']
        fileExtension = os.path.basename(
            urlparse(request.url).path).split('.')[-1]

        fileName = f'{title}.{fileExtension}'
        target_path = os.path.join(podcast_name, fileName)
        return target_path

    def item_completed(self, results, item, info):
        print("ITEM COMPLETES")
        print("RESULTS", results)

        for result in [x for ok, x in results if ok]:
            image_storage_path = get_project_settings().get('IMAGES_STORE')
            image_path = item.get('images')[0]['path']
            full_image_path = os.path.join(image_storage_path, image_path)
            print('FULL IMAGE PATH', full_image_path)

            file_storage_path = get_project_settings().get('FILES_STORE')
            podcast_path = result['path']
            full_podcast_path = os.path.join(file_storage_path, podcast_path)
            print('FULL PODCAST PATH')

            audiofile = eyed3.load(full_podcast_path)

            if (audiofile.tag == None):
                audiofile.initTag()

            audiofile.tag.images.set(
                3, open(full_image_path, 'rb').read(), 'image/jpeg')

            # audiofile.tag.images.set(type_=3, img_data=None, mime_type=None,
            #  img_url=item.get('cover_image'))

            audiofile.tag.artist = item.get('podcast_author')
            audiofile.tag.album_artist = item.get('podcast_author')
            audiofile.tag.album = item.get('podcast_name')
            audiofile.tag.title = item.get('title')
            # audiofile.tag.track_num = 2

            audiofile.tag.save()

            # target_path = os.path.join(
            #     storage_path, podcast_name, fileName)
            # print('TARGET PATH', target_path)
            # path = os.path.join(storage_path, path)

            # # If path doesn't exist, it will be created
            # if not os.path.exists(os.path.join(storage_path, podcast_name)):
            #     print("MAKE NEW DIRECTORY")
            #     os.makedirs(os.path.join(storage_path, podcast_name))

            # if not os.rename(path, target_path):
            #     raise DropItem("Could not move image to target folder")

        if self.FILES_RESULT_FIELD in item.fields:
            item[self.FILES_RESULT_FIELD] = [x for ok, x in results if ok]
        return item


# def toKebabCase(st):
#     return st.lower().replace(' ', '-')
