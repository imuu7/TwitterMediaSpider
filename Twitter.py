# -*- coding: utf-8 -*-
import os
import json
import time
from tqdm import tqdm
from modules.Videodler import Videodler
from modules.EZgif import Gif
from modules.net_fn import Net


class Twitter:

    def __init__(self, name, tweet_count=20, folder_path='./'):
        self.TwitterName = name
        self.count = tweet_count
        self.Videodler = Videodler()
        self.Gif = Gif()
        self.Net = Net()
        self.Headers = ""
        self.Proxy = "127.0.0.1:9999"
        self.Proxy = None
        self.FolderPath = f'{folder_path}{name}/'
        self.LogPath = f'./log/{name}.json'
        self.Log = []
        self.init()

    def init(self):
        # 設定Header
        with open('./token.json', 'r') as f:
            token = json.load(f)['token']
        self.Headers = f'Host: twitter.com###Connection: keep-alive###sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"###x-twitter-client-language: zh-tw###x-csrf-token: b53d6ae747724d57c50aa29b857f98a780756ba19ca415b412b2ae6a57aa6fe3501c550b94a183fee05c246435676a0c639679f6b42092faa8aa81f518db863f38861c4d0464ddae6fe7befde52a1c45###sec-ch-ua-mobile: ?0###authorization: Bearer {token}###content-type: application/json###User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36###x-twitter-auth-type: OAuth2Session###x-twitter-active-user: yes###sec-ch-ua-platform: "Windows"###Accept: */*###Sec-Fetch-Site: same-origin###Sec-Fetch-Mode: cors###Sec-Fetch-Dest: empty###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        cookie = 'Cookie: personalization_id="v1_clQL3pipYkKKmRw/xeF9Qw=="; guest_id=v1%3A162412431792724016; dnt=1; ads_prefs="HBESAAA="; kdt=cYWMKDcDO39ZltScrusapy7iyuy4eHt73mxNoceQ; remember_checked_on=1; auth_token=ed189145887898b4763a26f158f82939348eafa4; twid=u%3D701368575517265921; ct0=b53d6ae747724d57c50aa29b857f98a780756ba19ca415b412b2ae6a57aa6fe3501c550b94a183fee05c246435676a0c639679f6b42092faa8aa81f518db863f38861c4d0464ddae6fe7befde52a1c45; guest_id_marketing=v1%3A162412431792724016; guest_id_ads=v1%3A162412431792724016; mbox=session#d3b350f5a1064066844f5ad0c718a0da#1637175214|PC#d3b350f5a1064066844f5ad0c718a0da.32_0#1700418570; external_referer=padhuUp37zjSzNXpb3CVCQ%3D%3D|0|8e8t2xd8A2w%3D'
        self.Headers += f'###{cookie}'

        # 創建目錄(如果不存在)
        os.makedirs(self.FolderPath, exist_ok=True)
        os.makedirs(f'{self.FolderPath}image/', exist_ok=True)
        os.makedirs(f'{self.FolderPath}gif/', exist_ok=True)
        os.makedirs(f'{self.FolderPath}video/', exist_ok=True)

        # 讀取紀錄
        if os.path.isfile(self.LogPath):
            print("\nLoading log...")
            self.Log = json.load(open(self.LogPath))
        else:
            # 第一次爬先爬最多筆
            self.count = 500
            print("\nCreate new log...")

    def get_user_id(self):
        url = f'https://twitter.com/i/api/graphql/7mjxD3-C6BxitPMVQ6w0-Q/UserByScreenName?variables=%7B%22screen_name%22%3A%22{self.TwitterName}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D'

        result = self.Net.Get(url=url, header_string=self.Headers, proxy_ip=self.Proxy)

        user_id = result.json()['data']['user']['result']['rest_id']

        return user_id

    def get_all_media(self):
        url = f'https://twitter.com/i/api/graphql/8mbShRQN_rNuDMWVchLUPA/UserMedia?variables=%7B%22userId%22%3A%22{self.get_user_id()}%22%2C%22count%22%3A{self.count}%2C%22withTweetQuoteCount%22%3Afalse%2C%22includePromotedContent%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%7D'

        result = self.Net.Get(url=url, header_string=self.Headers, proxy_ip=self.Proxy)

        print('\nMedia information is complete.')

        return result.json()['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']

    def sort_media(self):
        media_object = self.get_all_media()[:-2]
        all_image = []
        all_gif = []
        all_vidoe = []
        exception = []
        for item in media_object:
            park = {
                'sort_index': item["sortIndex"],
                'tweet_url': f'https://twitter.com/{self.TwitterName}/status/{item["sortIndex"]}'
            }
            if item['content']['itemContent']['tweet_results'] == {}:
                park['type'] = 'other'
                exception.append(park)
                continue
            tweet = item['content']['itemContent']['tweet_results']['result']['legacy']
            if 'extended_entities' not in tweet:
                park['type'] = 'other'
                exception.append(park)
                continue
            media_list = tweet['extended_entities']['media']
            type = media_list[0]['type']
            if type == 'photo':
                park['type'] = 'image'
                url_list = []
                for image in media_list:
                    url_list.append(image['media_url_https'])
                park['media_url'] = url_list
                all_image.append(park)
            elif type == 'animated_gif':
                park['type'] = 'gif'
                all_gif.append(park)
            elif type == 'video':
                park['type'] = 'video'
                all_vidoe.append(park)
            else:
                print(f'https://twitter.com/{self.TwitterName}/status/{item["sortIndex"]}\n')
        print('\nMedia information is sort out.\n')
        return {'image': all_image, 'gif': all_gif, 'video': all_vidoe, 'other': exception}

    def download_media(self, url, type):
        name = url.split("/")[-1]
        if type == 'gif':
            name = f'{name.split(".")[0]}.gif'
            url = self.Gif.download_gif(url)
        rs = self.Net.Get(url=url)

        with open(f'{self.FolderPath}{type}/{name}', 'wb') as fp:
            fp.write(rs.content)

    def save_log(self):
        media_json = self.sort_media()
        image_count = 0
        gif_count = 0
        video_count = 0
        print('Image：')
        time.sleep(1)
        for item in tqdm(media_json['image']):
            if item['sort_index'] not in self.Log:
                self.Log.append(item['sort_index'])
                for link in item['media_url']:
                    self.download_media(link, 'image')
                    image_count += 1
                    time.sleep(0.1)
        print('Gif：')
        time.sleep(1)
        for item in tqdm(media_json['gif']):
            if item['sort_index'] not in self.Log:
                link = self.Videodler.download_video(item['tweet_url'])
                if link:
                    self.download_media(link, 'gif')
                    self.Log.append(item['sort_index'])
                else:
                    print(f'\nFail Link：{item["tweet_url"]}')
                    continue
                gif_count += 1
            time.sleep(1.5)
        print('Video：')
        time.sleep(1)
        for item in tqdm(media_json['video']):
            if item['sort_index'] not in self.Log:
                link = self.Videodler.download_video(item['tweet_url'])
                if link:
                    self.download_media(link, 'video')
                    self.Log.append(item['sort_index'])
                else:
                    print(f'\nFail Link：{item["tweet_url"]}')
                    continue
                video_count += 1
            time.sleep(1.5)

        with open(self.LogPath, 'w') as fp:
            json.dump(self.Log, fp)

        print(f'\nImage：{image_count}\nGif：{gif_count}\nVideo：{video_count}')


if __name__ == '__main__':
    name = input('Please enter Twitter name：')
    t = Twitter(name=name)
    # print(t.get_user_id())
    # print(json.dumps(t.get_all_media()))
    # print(json.dumps(t.sort_media()))
    t.save_log()
