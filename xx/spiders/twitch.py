# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request

class TwitchSpider(Spider):
    name = 'twitch'
    allowed_domains = ['twitch.tv']
    start_urls = ['https://gql.twitch.tv/gql']

    def parse(self, response):
        pritn("xxx")

    def start_requests(self):
        for url in self.start_urls:          
            yield Request(url, cookies={'techbrood.com': 'true'})  

