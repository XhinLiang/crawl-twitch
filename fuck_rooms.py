# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import json
import urllib
from urllib.parse import urlencode


cmd_pubg = '''
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H $'Referer: https://www.twitch.tv/directory/game/PLAYERUNKNOWN\\\'S%20BATTLEGROUNDS' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary $'[{"variables":{"name":"PLAYERUNKNOWN\\\'S BATTLEGROUNDS","limit":30,"languages":[],"type":"GAME","filters":{"hearthstoneBroadcasterHeroName":"","hearthstoneBroadcasterHeroClass":"","hearthstoneGameMode":"","overwatchBroadcasterCharacter":"","leagueOfLegendsChampionID":"","counterStrikeMap":"","counterStrikeSkill":""}XHINLIANG_CURSOR},"extensions":{},"operationName":"GamePage_Game","query":"query GamePage_Game($name: String!, $type: DirectoryType!, $limit: Int, $languages: [String!], $cursor: Cursor, $filters: StreamMetadataFilterInput) {  directory(name: $name, type: $type) {    id    displayName    ... on Community {      id      streams(first: $limit, after: $cursor, languages: $languages) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    ... on Game {      id      streams(first: $limit, after: $cursor, languages: $languages, filters: $filters) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            streamMetadata {              counterStrikeGlobalOffensive {                skill                __typename              }              hearthstone {                broadcasterHeroClass                __typename              }              overwatch {                broadcasterCharacter                __typename              }              leagueOfLegends {                championID                summonerDivision                summonerID                summonerName                summonerRank                __typename              }              __typename            }            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    __typename  }}"}]' --compressed
'''
cmd_pubg = cmd_pubg.replace("\\\n", "")

cmd = '''
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H $'Referer: https://www.twitch.tv/directory/game/GAME_NAME_URLENCODED' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary $'[{"variables":{"name":"GAME_NAME_RAW","limit":30,"languages":[],"type":"GAME","filters":{"hearthstoneBroadcasterHeroName":"","hearthstoneBroadcasterHeroClass":"","hearthstoneGameMode":"","overwatchBroadcasterCharacter":"","leagueOfLegendsChampionID":"","counterStrikeMap":"","counterStrikeSkill":""}XHINLIANG_CURSOR},"extensions":{},"operationName":"GamePage_Game","query":"query GamePage_Game($name: String!, $type: DirectoryType!, $limit: Int, $languages: [String!], $cursor: Cursor, $filters: StreamMetadataFilterInput) {  directory(name: $name, type: $type) {    id    displayName    ... on Community {      id      streams(first: $limit, after: $cursor, languages: $languages) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    ... on Game {      id      streams(first: $limit, after: $cursor, languages: $languages, filters: $filters) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            streamMetadata {              counterStrikeGlobalOffensive {                skill                __typename              }              hearthstone {                broadcasterHeroClass                __typename              }              overwatch {                broadcasterCharacter                __typename              }              leagueOfLegends {                championID                summonerDivision                summonerID                summonerName                summonerRank                __typename              }              __typename            }            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    __typename  }}"}]' --compressed
'''
cmd = cmd.replace("\\\n", "")

map = {}


def fuck_room(game_name, cursor=None):
    if cursor is not None:
        c = cmd.replace('XHINLIANG_CURSOR', ',"cursor":"%s"' % cursor)
    else:
        c = cmd.replace('XHINLIANG_CURSOR', '')
    c = c.replace('GAME_NAME_RAW', game_name)
    c = c.replace('GAME_NAME_URLENCODED', urllib.parse.quote(game_name))
    with open("temp.sh", "w") as f:
        f.write(c)
    try:
        output = subprocess.check_output("bash temp.sh", shell=True)
    except:
        return json.loads("{}"), "xx", False
    output = output.decode('utf8')
    json_object = json.loads(output)
    edges = json_object[0]['data']['directory']['streams']['edges']
    if game_name in map:
        map[game_name] = map[game_name] + len(edges)
    else:
        map[game_name] = len(edges)
    print(game_name + " " + str(map[game_name]))
    if len(edges) == 0:
        return json.loads("{}"), "xx", False
    last_object = edges[-1]
    last_cursor = last_object['cursor']
    has_next_page = json_object[0]['data']['directory']['streams']['pageInfo']['hasNextPage']
    return json_object, last_cursor, has_next_page


def fuck_game(name):
    name = name.replace("'", "\\'")
    should_continue = True
    page = 1
    cursor = None
    while should_continue:
        j, cursor, should_continue = fuck_room(name, cursor)
        page = page + 1
    if name in map:
        print("%s %d" % (name, map[name]))
        with open("count.csv", "a") as f:
            f.write("%s %d\n" % (name, map[name]))


from os import listdir
from os.path import isfile, join

mypath = 'games'

json_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
json_files.sort()
for json_file in json_files:
    with open('games/' + json_file, 'r') as f:
        data = json.load(f)
        for edge in data[0]['data']['directories']['edges']:
            try:
                name = edge['node']['name']
                fuck_game(name)
            except:
                print("name UnicodeEncodeError")
