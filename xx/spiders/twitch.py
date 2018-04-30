# -*- coding: utf-8 -*-
from scrapy.http.request import Request
from scrapy.spider import Spider
import json

body = '[{"variables":{"limit":30,"directoryFilters":["GAMES"],"directorySort":"VIEWER_COUNT", COURSOR_REPLACE},"extensions":{},"operationName":"BrowsePage_AllDirectories","query":"query BrowsePage_AllDirectories($limit: Int, $cursor: Cursor, $directoryFilters: [DirectoryFilter!], $directorySort: DirectorySort) {  directories(first: $limit, after: $cursor, filterBySet: $directoryFilters, sortBy: $directorySort) {    edges {      cursor      node {        id        displayName        name        avatarURL(width: 285, height: 380)        viewersCount        directoryType        ... on Game {          activeDropCampaigns {            applicableChannels {              id              __typename            }            __typename          }          __typename        }        __typename      }      __typename    }    pageInfo {      hasNextPage      __typename    }    __typename  }}"}]'
cursorxx = ',"cursor":"NjQ4"'


class TwitchSpider(Spider):
    name = 'twitch'
    allowed_domains = ['twitch.tv']
    start_urls = ['https://gql.twitch.tv/gql']
    cursor = ""

    def parse(self, response):
        print("xxx")

    def build_body(self):
        b = body.replace('COURSOR_REPLACE', self.cursor)
        return b

    def start_requests(self):
        yield Request('https://gql.twitch.tv/gql', method='POST', cookies={'techbrood.com': 'true'},
                      headers={
                          'Host': 'gql.twitch.tv',
                          'Connection': 'keep-alive',
                          'Content-Length': '932',
                          'Origin': 'https://www.twitch.tv',
                          'Accept-Language': 'zh-CN',
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                          'Content-Type': 'application/json',
                          'Accept': '*/*',
                          'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                          'X-Device-Id': '3bafce6fee4ebbed',
                          'Referer': 'https://www.twitch.tv/directory',
                          'Accept-Encoding': 'gzip, deflate, br'},
                      body=self.build_body())
