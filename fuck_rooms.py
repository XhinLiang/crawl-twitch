# -*- coding: utf-8 -*-

import json
import subprocess
import urllib
import sys
from concurrent.futures import ThreadPoolExecutor
from os import listdir
from os.path import isfile, join, devnull
from queue import Queue
from threading import Thread
from urllib.parse import urlencode

cmd = '''
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H $'Referer: https://www.twitch.tv/directory/game/GAME_NAME_URLENCODED' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary $'[{"variables":{"name":"GAME_NAME_RAW","limit":30,"languages":[],"type":"GAME","filters":{"hearthstoneBroadcasterHeroName":"","hearthstoneBroadcasterHeroClass":"","hearthstoneGameMode":"","overwatchBroadcasterCharacter":"","leagueOfLegendsChampionID":"","counterStrikeMap":"","counterStrikeSkill":""}XHINLIANG_CURSOR},"extensions":{},"operationName":"GamePage_Game","query":"query GamePage_Game($name: String!, $type: DirectoryType!, $limit: Int, $languages: [String!], $cursor: Cursor, $filters: StreamMetadataFilterInput) {  directory(name: $name, type: $type) {    id    displayName    ... on Community {      id      streams(first: $limit, after: $cursor, languages: $languages) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    ... on Game {      id      streams(first: $limit, after: $cursor, languages: $languages, filters: $filters) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            streamMetadata {              counterStrikeGlobalOffensive {                skill                __typename              }              hearthstone {                broadcasterHeroClass                __typename              }              overwatch {                broadcasterCharacter                __typename              }              leagueOfLegends {                championID                summonerDivision                summonerID                summonerName                summonerRank                __typename              }              __typename            }            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    __typename  }}"}]' --compressed
'''
cmd = cmd.replace("\\\n", "")


def fuck_room(game_name, cursor, queue, pool):
    if cursor is not None:
        c = cmd.replace('XHINLIANG_CURSOR', ',"cursor":"%s"' % cursor)
    else:
        c = cmd.replace('XHINLIANG_CURSOR', '')
    c = c.replace('GAME_NAME_RAW', game_name)
    c = c.replace('GAME_NAME_URLENCODED', urllib.parse.quote(game_name))
    with open(devnull, 'w') as dn:
        output = subprocess.check_output(c, shell=True, stderr=dn)
    output = output.decode('utf8')
    json_object = json.loads(output)
    edges = json_object[0]['data']['directory']['streams']['edges']
    if len(edges) == 0:
        queue.put([game_name, -1])
        return
    last_object = edges[-1]
    last_cursor = last_object['cursor']
    has_next_page = json_object[0]['data']['directory']['streams']['pageInfo']['hasNextPage']
    queue.put([game_name, len(edges)])
    if not has_next_page:
        queue.put([game_name, -1])
        return
    pool.submit(fuck_room, game_name, last_cursor, queue, pool)


def fuck_game(name, queue, pool):
    name = name.replace("'", "\\'")
    pool.submit(fuck_room, name, None, queue, pool)


def main():
    pool = ThreadPoolExecutor(128)
    games_path = 'games'

    queue = Queue()

    def write_count(q):
        m = {}
        with open("game_rooms_count.csv", "w", encoding='utf-8') as f:
            while True:
                d = q.get()
                n, c = d[0], d[1]
                sys.stdout.write(".")
                sys.stdout.flush()
                if c != -1:
                    if n not in m:
                        m[n] = d[1]
                    else:
                        m[n] = m[n] + c
                else:
                    if n not in m:
                        m[n] = 0
                    sys.stdout.write("%s, %d\n" % (n, m[n]))
                    f.write("%s, %d\n" % (n, m[n]))
                    f.flush()

    write_thread = Thread(target=write_count, args=(queue,))
    write_thread.setDaemon(True)
    write_thread.start()

    json_files = [f for f in listdir(games_path) if isfile(join(games_path, f))]
    json_files.sort()
    for json_file in json_files:
        with open('games/' + json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for edge in data[0]['data']['directories']['edges']:
                name = edge['node']['name']
                fuck_game(name, queue, pool)


if __name__ == '__main__':
    main()
