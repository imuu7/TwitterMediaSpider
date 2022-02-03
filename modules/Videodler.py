# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
from modules.net_fn import Net


class Videodler:

    def __init__(self):
        self.Net = Net()
        self.Headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        self.Proxy = "127.0.0.1:9999"
        self.Proxy = None
        self.Session = requests.Session()

    def get_token(self):
        url = 'https://videodler.com/twitter/en'
        result = self.Net.Get(url=url, header_string=self.Headers, proxy_ip=self.Proxy, sess=self.Session)
        if result == None:
            result = self.Net.Get(url=url, header_string=self.Headers, proxy_ip=self.Proxy, sess=self.Session)
        page = pq(result.text)
        page_div = page("#form_download > div > input[type=hidden]")
        token = page_div.val()

        return token

    def download_video(self, tweet_url):
        url = 'https://videodler.com/twitter/en/download'
        data = {'url': tweet_url, '_token': self.get_token()}
        result = self.Net.Poster(url=url, header_string=self.Headers, proxy_ip=self.Proxy, data=data, sess=self.Session)
        if result == None:
            result = self.Net.Poster(url=url, header_string=self.Headers, proxy_ip=self.Proxy, data=data, sess=self.Session)
        page = pq(result.text)

        page_div = page(".dropbox-saver")
        if len(page_div) < 1:
            return None
        download_link = page_div.attr('href').split("?")[0]
        return download_link


if __name__ == '__main__':
    obj = Videodler()
    # print(obj.get_token())
    print(obj.download_video('https://twitter.com/sonwooang/status/1423252232498081793'))
    # print(obj.download_video('https://twitter.com/sonwooang/status/1459500462755893252'))
