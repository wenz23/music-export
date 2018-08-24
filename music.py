import requests
import json
from urllib import urlopen
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import webbrowser

netEaseUrl = "https://api.hibai.cn/api/index/index"

netEasePlaylistId = "28880687"
doubanCookieString = 'flag="ok"; bid=IboTqM7Flow; dbcl2="76336310:Ui2X7wyJF44"; ck=TKC0; _ga=GA1.2.1056722382.1535143886; _gid=GA1.2.189738775.1535143886; _gat=1'

# Request for netease related content
payload = json.dumps({
  "TransCode": "020111",
  "OpenId": "123456789",
  "Body": {
    "SongListId": netEasePlaylistId 
  }
})

headers = {'content-type': 'application/json'}

querystring = {"id": netEasePlaylistId}

response = requests.request("POST", netEaseUrl, data=payload, headers=headers)

musics = []

filter = set()

if response.status_code == 200:
  content = json.loads(response.text)
  for track in content["Body"]["songs"]:
    musics.append(track['title'] + ' - ' + track['author'])
    filter.add(track['title'].lower().strip())

# Request douban related content
doubanCookies = {}
for cookie in doubanCookieString.split(';'):
  key = cookie.split('=')[0].strip()
  value = cookie.split('=')[1].strip()
  doubanCookies[key] = value

doubanUrl = "https://douban.fm/j/v2/redheart/basic"
response = requests.post(doubanUrl, cookies=doubanCookies)
doubanSongList = []
if response.status_code == 200:
  content = json.loads(response.text)
  for c in content['songs']:
    doubanSongList.append(c['sid'])

redheartUrl = "https://douban.fm/j/v2/redheart/songs"
songIds = []
for i, sid in enumerate(doubanSongList):
  
  if i % 20 == 19:
    payload = "sids=" + '|'.join(songIds)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", redheartUrl, data=payload, headers=headers, cookies=doubanCookies)
    if response.status_code == 200:
      content = json.loads(response.text)
      for c in content:
        title = c['title']
        if title.lower().strip() in filter:
          continue
        filter.add(title.lower().strip())
        musics.append(title + ' - ' + c['singers'][0]['name'])
    else:
      print "Error fetching the douban music list"
    songIds = [sid]
  else:
    songIds.append(sid)

content = '\n'.join(musics)

with open('music.txt', 'w') as f:
  f.write('\n'.join(musics))

url = 'http://spotlistr.herokuapp.com/#/search/textbox'
webbrowser.open(url)
