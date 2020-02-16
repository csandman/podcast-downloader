# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class Podcast(Item):
    # main podcast details
    podcast_name = Field()
    podcast_author = Field()
    podcast_description = Field()

    # episode details
    id = Field()
    filename = Field()
    title = Field()
    track_num = Field()
    description = Field()
    episode_number = Field()
    cover_image = Field()

    # downloaded files
    file_urls = Field()
    files = Field()
    image_urls = Field()
    images = Field()
