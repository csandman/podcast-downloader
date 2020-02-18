import scrapy
import json
import re
from podcast_scraper.items import Podcast
from scrapy.exceptions import DropItem
from datetime import datetime

# https://podbay.fm/api/podcast?id=318185524&refresh=true


class PodbaySpider(scrapy.Spider):
    name = "podbay"
    page_num = 0
    base_url = 'https://podbay.fm/podcast/318185524'
    ajax_base_url = ''

    podcase_name = ''
    podcast_author = ''
    podcast_description = ''

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse_main_page)

    def parse_main_page(self, response):
        self.podcast_name = response.css(
            '.main-meta .title::text').get().strip()
        self.podcast_author = response.css(
            '.main-meta .author::text').get().strip()
        self.podcast_description = response.css(
            '.main-meta .description::text').get().strip()
        # print('\n\n', self.podcast_name, '\n\n')
        idRegex = re.compile(r'\d+')
        podcast_id = getSubstr(self.base_url, idRegex)
        self.ajax_base_url = f'https://podbay.fm/api/episodes?podcastID={podcast_id}'
        yield scrapy.Request(url=f'{self.ajax_base_url}&page={self.page_num}', callback=self.parse_podcasts)

    def parse_podcasts(self, response):
        result = json.loads(response.body_as_unicode())
        episodes = result["episodes"]
        if (episodes):
            for episode in episodes:
                yield self.parse_podcast(episode)
            # self.page_num += 1
            # yield scrapy.Request(url=f'{self.ajax_base_url}&page={self.page_num}', callback=self.parsePodcasts)

    def parse_podcast(self, podcastDict):
        podcast = Podcast()

        # SET MAIN PODCAST ATTRIBUTES
        podcast["podcast_name"] = self.podcast_name
        podcast["podcast_author"] = self.podcast_author
        podcast["podcast_description"] = self.podcast_description

        # GET ID
        podcast["id"] = podcastDict["_id"]

        # GET FULL TITLE
        podcast["title"] = podcastDict['title']

        # GET DESCRIPTION
        podcast["description"] = podcastDict['description']

        # GET RELEASE DATE
        podcast["release_date"] = datetime.strptime(
            podcastDict['published'], '%Y-%m-%dT%H:%M:%S.%fZ')

        # GET MP3
        # images = []
        # for image in podcastDict["images"]:
        #     images.append(image["src"].split('?')[0])
        podcast["file_urls"] = [podcastDict['enclosure']['url']]

        # GET image
        # for image in podcastDict["images"]:
        #     images.append(image["src"].split('?')[0])
        podcast["image_urls"] = [podcastDict['image']]

        podcast['cover_image'] = podcastDict['image']

        # # GET BRAND
        # podcast["brand"] = podcastDict["vendor"]

        # # GET SKU
        # podcast["sku"] = podcastDict["variants"][0]["sku"]

        # # GET URL
        # podcast["url"] = '%s/products/%s' % (self.base_url,
        #                                      podcastDict["handle"])

        # # GET STRIPPED TITLE
        # titleArr = podcastDict['title'].split(' Deck-')

        # if len(titleArr) == 1:
        #     titleArr = podcastDict['title'].split('-')

        # plainTitle = titleArr[0].replace(podcastDict["vendor"], "").strip()

        # # GET YEAR FROM TITLE
        # yearRegex = re.compile(r"(19|20)\d{2}")
        # year = getSubstr(plainTitle, yearRegex)

        # if len(year) > 0:
        #     podcast["year"] = int(year)
        #     plainTitle = re.sub(r"(19|20)\d{2}", "", plainTitle).strip()

        # podcast["name"] = plainTitle

        # # GET DIMENSIONS
        # if 1 < len(titleArr):
        #     dimensions = getAllNumbers(titleArr[1])
        #     if len(dimensions) > 0:
        #         podcast["width"] = dimensions[0]
        #     if len(dimensions) > 1:
        #         podcast["length"] = dimensions[1]

        # # GET PRICES
        # if "compare_at_price" in podcastDict["variants"][0]:
        #     podcast["sale_price"] = getNumber(
        #         podcastDict["variants"][0]["price"])
        #     podcast["price"] = getNumber(
        #         podcastDict["variants"][0]["compare_at_price"])
        # else:
        #     podcast["price"] = getNumber(podcastDict["variants"][0]["price"])

        return podcast


def getAllNumbers(st, nType="float"):
    if nType == "float":
        numberStrings = re.findall(r"\d*\.\d+|\d+", st)
        return list(map(lambda x: float(x), numberStrings))
    elif nType == "int":
        numberStrings = re.findall(r"\d+", st)
        return list(map(lambda x: int(x), numberStrings))


def getNumber(st, nType="float"):
    if nType == "float":
        return float(re.sub(r"[^0-9\.]", "", st))
    elif nType == "int":
        return int(re.sub(r"[^0-9\.]", "", st))


def toKebabCase(st):
    return st.lower().replace(' ', '-')


def getSubstr(strToSearch, regex):
    result = regex.search(strToSearch)
    if result:
        return result.group(0)
    else:
        return ""
