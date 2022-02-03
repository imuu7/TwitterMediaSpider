import random
import string
import time
from pyquery import PyQuery as pq
from modules.net_fn import Net


class Gif:

    def __init__(self):
        self.Net = Net()
        self.Headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        self.Proxy = "127.0.0.1:9999"
        self.Proxy = None
        self.content_boundary = ''.join(random.sample(string.ascii_letters + string.digits, 16))

    def get_detail(self, link):
        url = 'https://s6.ezgif.com/video-to-gif'
        header_string = f"""Connection: keep-alive###Content-Length: 454###Cache-Control: max-age=0###sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"###sec-ch-ua-mobile: ?0###sec-ch-ua-platform: "Windows"###Upgrade-Insecure-Requests: 1###Origin: https://ezgif.com###Content-Type: multipart/form-data; boundary=----WebKitFormBoundary{self.content_boundary}###User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9###Sec-Fetch-Site: same-site###Sec-Fetch-Mode: navigate###Sec-Fetch-User: ?1###Sec-Fetch-Dest: document###Referer: https://ezgif.com/###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"""
        data = f'------WebKitFormBoundary{self.content_boundary}\r\nContent-Disposition: form-data; name="new-image-url"\r\n\r\n{link}\r\n------WebKitFormBoundary{self.content_boundary}\r\nContent-Disposition: form-data; name="upload"\r\n\r\nUpload video!'
        # time.sleep(1.5)
        result = self.Net.Poster(url=url, header_string=header_string, proxy_ip=self.Proxy, data=data)
        if result == None:
            result = self.Net.Poster(url=url, header_string=header_string, proxy_ip=self.Proxy, data=data)
        page = pq(result.text)
        file = page("input[name=file]").val()
        token = page("input[name=token]").val()
        start = page("input[name=start]").val()
        end = page("input[name=end]").val()

        return {'file': file, 'token': token, 'start': start, 'end': end}

    def set_fps(self, url, header_string, data):
        fps = [25, 20, 12, 10, 7, 5]
        n = 0
        while n < 6:
            data['fps'] = fps[n]
            time.sleep(1.5)
            result = self.Net.Poster(url=url, header_string=header_string, proxy_ip=self.Proxy, data=data)
            if result == None:
                pass
            else:
                if result.text.split(".")[0] == 'Please specify shorter GIF duration or lower frame rate':
                    n += 1
                else:
                    return result

        print(url)
        exit()

    def download_gif(self, link):
        detail = self.get_detail(link)
        url = f"https://s6.ezgif.com/video-to-gif/{detail['file']}?ajax=true"
        header_string = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        data = {
            'file': detail['file'],
            'token': detail['token'],
            'start': detail['start'],
            'end': detail['end'],
            'size': 800,
            'fps': None,
            'method': 'ffmpeg',
        }
        result = self.set_fps(url=url, header_string=header_string, data=data)

        page = pq(result.text)
        download_link = f'https:{page("p > img").attr("src")}'

        return download_link


if __name__ == '__main__':
    obj = Gif()
    # print(obj.get_detail('https://video.twimg.com/tweet_video/E8BoNzBVUAUFVIL.mp4'))
    print(obj.download_gif('https://video.twimg.com/tweet_video/E8BoNzBVUAUFVIL.mp4'))
