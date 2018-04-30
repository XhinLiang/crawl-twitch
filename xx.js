const constCmd = `
curl 'https://gql.twitch.tv/gql' -H 'Origin: https://www.twitch.tv' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: zh-CN' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'Referer: https://www.twitch.tv/directory/game/GAME_NAME_URLENCODED' -H 'Connection: keep-alive' -H 'Client-Id: kimne78kx3ncx6brgo4mv6wki5h1ko' -H 'X-Device-Id: 3bafce6fee4ebbed' --data-binary '[{"variables":{"name":"GAME_NAME_RAW","limit":30,"languages":[],"type":"GAME","filters":{"hearthstoneBroadcasterHeroName":"","hearthstoneBroadcasterHeroClass":"","hearthstoneGameMode":"","overwatchBroadcasterCharacter":"","leagueOfLegendsChampionID":"","counterStrikeMap":"","counterStrikeSkill":""}XHINLIANG_CURSOR},"extensions":{},"operationName":"GamePage_Game","query":"query GamePage_Game($name: String!, $type: DirectoryType!, $limit: Int, $languages: [String!], $cursor: Cursor, $filters: StreamMetadataFilterInput) {  directory(name: $name, type: $type) {    id    displayName    ... on Community {      id      streams(first: $limit, after: $cursor, languages: $languages) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    ... on Game {      id      streams(first: $limit, after: $cursor, languages: $languages, filters: $filters) {        edges {          cursor          node {            id            title            viewersCount            previewImageURL(width: 320, height: 180)            broadcaster {              id              login              displayName              roles {                isPartner                __typename              }              profileImageURL(width: 50)              __typename            }            game {              id              boxArtURL(width: 40, height: 56)              name              __typename            }            type            streamMetadata {              counterStrikeGlobalOffensive {                skill                __typename              }              hearthstone {                broadcasterHeroClass                __typename              }              overwatch {                broadcasterCharacter                __typename              }              leagueOfLegends {                championID                summonerDivision                summonerID                summonerName                summonerRank                __typename              }              __typename            }            __typename          }          __typename        }        pageInfo {          hasNextPage          __typename        }        __typename      }      __typename    }    __typename  }}"}]' --compressed
`;

var fs = require('fs');


let fuckRoom = function (gameName, cursor, callback) {
  let c = constCmd.replace("XHINLIANG_CURSOR", '');
  if (cursor != null) {
    c = constCmd.replace("XHINLIANG_CURSOR", ',"cursor":"' + cursor + '"');
  }
  c = c.replace('GAME_NAME_RAW', gameName)
  c = c.replace('GAME_NAME_URLENCODED', encodeURIComponent(gameName))

  exec(c, (err, stdout, stderr) => {
    if (err) {
      // node couldn't execute the command
      console.log("error" + err);
      return;
    }

    // the *entire* stdout and stderr (buffered)
    console.log(`stdout: ${stdout}`);
    console.log(`stderr: ${stderr}`);
    callback(stdout);
  });
}

function fuckName(name, page) {
  let shouldContinue = true;
  let cursor = null;
  while (shouldContinue) {
    let fileName = 'xgame/' + name + "_" + page + ".json";
    if (fs.existsSync(path)) {
      // Do something
      fuckName(name, page + 1)
      continue;
    }
    fuckRoom(name, cursor, function (j, c, s) {
      fs.writeFile(fileName, JSON.stringify(j), function (err) {
        if (err) {
          return console.log(err);
        }
      });
      if (s) {
        fuckName(name, page + 1)
      }
    });
  }
}

fs.readdir('games', (err, files) => {
  files.sort();
  files.forEach(file => {
    data = fs.readFileSync("games/" + file);
    data = JSON.parse(data);
    for (edge in data[0]['data']['directories']['edges']) {
      name = edge['node']['name'];
      fuckName(name);
    }
  });
})

