# -*- coding: utf-8 -*-

import json
import subprocess
import urllib
from urllib.parse import urlencode
from os import listdir
from os.path import isfile, join
from concurrent.futures import ThreadPoolExecutor

cmd = '''
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H $'Referer: https://www.twitch.tv/directory/game/GAME_NAME_URLENCODED' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary $'[{"variables":{"name":"GAME_NAME_RAW","limit":30,"languages":[],"type":"GAME","filters":{"hearthstoneBroadcasterHeroName":"","hearthstoneBroadcasterHeroClass":"","hearthstoneGameMode":"","overwatchBroadcasterCharacter":"","leagueOfLegendsChampionID":"","counterStrikeMap":"","counterStrikeSkill":""}XHINLIANG_CURSOR},"extensions":{},"operationName":"GamePage_Game","query":"query GamePage_Game($name: String!, $type: DirectoryType!, $limit: Int, $languages: [String!], $cursor: Cursor, $filters: StreamMetadataFilterInput) {  directory(name: $name, type: $type) {    id    displayName    ... on Community {      id      streams(first: $limit, after: $cursor, languages: $languages) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    ... on Game {      id      streams(first: $limit, after: $cursor, languages: $languages, filters: $filters) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            streamMetadata {              counterStrikeGlobalOffensive {                skill                __typename              }              hearthstone {                broadcasterHeroClass                __typename              }              overwatch {                broadcasterCharacter                __typename              }              leagueOfLegends {                championID                summonerDivision                summonerID                summonerName                summonerRank                __typename              }              __typename            }            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    __typename  }}"}]' --compressed
'''
cmd = cmd.replace("\\\n", "")


def fuck_room(game_name, cursor=None):
    if cursor is not None:
        c = cmd.replace('XHINLIANG_CURSOR', ',"cursor":"%s"' % cursor)
    else:
        c = cmd.replace('XHINLIANG_CURSOR', '')
    c = c.replace('GAME_NAME_RAW', game_name)
    c = c.replace('GAME_NAME_URLENCODED', urllib.parse.quote(game_name))
    try:
        output = subprocess.check_output(c, shell=True)
    except:
        return json.loads("{}"), "xx", False, 0
    output = output.decode('utf8')
    json_object = json.loads(output)
    edges = json_object[0]['data']['directory']['streams']['edges']
    if len(edges) == 0:
        return json.loads("{}"), "xx", False, 0
    last_object = edges[-1]
    last_cursor = last_object['cursor']
    has_next_page = json_object[0]['data']['directory']['streams']['pageInfo']['hasNextPage']
    return json_object, last_cursor, has_next_page, len(edges)


def fuck_game(name):
    name = name.replace("'", "\\'")
    should_continue = True
    page = 1
    cursor = None
    count = 0
    while should_continue:
        j, cursor, should_continue, current_count = fuck_room(name, cursor)
        page = page + 1
        count = count + current_count
    print("%s %d" % (name, count))
    with open("count.csv", "a", encoding='utf-8') as f:
        f.write("%s, %d\n" % (name, count))


pool = ThreadPoolExecutor(128)
mypath = 'games'

json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
json_files.sort()
for json_file in json_files:
    with open('games/' + json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for edge in data[0]['data']['directories']['edges']:
            name = edge['node']['name']
            pool.submit(fuck_game, name)
