# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import json

cmd = '''
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'Referer: https://www.twitch.tv/directory' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary '[{"variables":{"limit":30,"directoryFilters":["GAMES"],"directorySort":"VIEWER_COUNT"XHINLIANG},"extensions":{},"operationName":"BrowsePage_AllDirectories","query":"query BrowsePage_AllDirectories($limit: Int, $cursor: Cursor, $directoryFilters: [DirectoryFilter!], $directorySort: DirectorySort) {  directories(first: $limit, after: $cursor, filterBySet: $directoryFilters, sortBy: $directorySort) {    edges {      cursor      node {        id        displayName        name        avatarURL(width: 285, height: 380)        viewersCount        directoryType        ... on Game {          activeDropCampaigns {            applicableChannels {              id              __typename            }            __typename          }          __typename        }        __typename      }      __typename    }    pageInfo {      hasNextPage      __typename    }    __typename  }}"}]' --compressed
'''
cmd = cmd.replace('\\n', '')


def xx(cursor=None):
    if cursor is not None:
        c = cmd.replace('XHINLIANG', ',"cursor":"%s"' % cursor)
    else:
        c = cmd.replace('XHINLIANG', '')
    output = subprocess.check_output(c, shell=True)
    output = output.decode('utf8')
    json_object = json.loads(output)
    last_object = json_object[0]['data']['directories']['edges'][-2]
    last_cursor = last_object['cursor']
    has_next_page = json_object[0]['data']['directories']['pageInfo']['hasNextPage']
    return json_object, last_cursor, has_next_page


should_continue = True
page = 1
cursor = None
while should_continue:
    j, cursor, should_continue = xx(cursor)
    with open("games/" + str(page) + ".json", 'w') as f:
        f.write(json.dumps(j, indent=4, sort_keys=True))
    page = page + 1
