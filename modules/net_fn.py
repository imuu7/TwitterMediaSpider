# -*- coding: UTF-8 -*-
import sys
import os
import urllib3
import requests
import re
from requests.adapters import HTTPAdapter
import requests.sessions as sessions
requests.adapters.DEFAULT_RETRIES = 2
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.TimeoutError)
urllib3.disable_warnings(urllib3.exceptions.MaxRetryError)


class Net:
    def __init__(self):
        pass

    def Get(
            self,
            url,
            header_string="",
            cookie="",
            SSL_verify=0,
            timeout=5,
            proxy_ip=None,
            params=None,
            sess=None,
            allow_redirects=True):
        header_dict = self.get_header_dict(header_string)

        try:
            if proxy_ip is not None:
                proxies = {
                    "http": "{}".format(proxy_ip),
                    "https": "{}".format(proxy_ip),
                }
                if sess is None:
                    rs = requests.get(
                        url,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        proxies=proxies,
                        params=params,
                        allow_redirects=allow_redirects)
                else:
                    rs = sess.get(
                        url,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        proxies=proxies,
                        params=params,
                        allow_redirects=allow_redirects)
            else:
                if sess is None:
                    rs = requests.get(
                        url,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        params=params,
                        allow_redirects=allow_redirects)
                else:
                    rs = sess.get(
                        url,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        params=params,
                        allow_redirects=allow_redirects)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print("failwe")
            return None

        return rs

    def Poster_form_Data(
            self,
            url,
            data={},
            header_string="",
            cookie="",
            SSL_verify=0,
            timeout=5,
            proxy_ip=None,
            boundary="",
            sess=None):
        headers = self.get_header_dict(header_string)
        payload = {}

        for key in data:
            payload[key] = (None, str(data[key]))

        if proxy_ip is None:
            proxy = urllib3.PoolManager()
        else:
            print("http://{}/".format(proxy_ip))
            proxy = urllib3.ProxyManager("http://{}".format(proxy_ip))
        print(payload)
        if sess is None:
            rs = proxy.request(
                'POST',
                url,
                fields=payload,
                headers=headers,
                multipart_boundary=boundary)
        else:
            rs = sess.request(
                'POST',
                url,
                fields=payload,
                headers=headers,
                multipart_boundary=boundary)
        # print(rs.status)
        return rs

    def download_file(self, url, filepath, timeout=50 * 60):
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return filepath

    def Poster(
            self,
            url,
            data={},
            json=None,
            files={},
            header_string="",
            cookie="",
            SSL_verify=0,
            timeout=5,
            proxy_ip=None,
            params=None,
            sess=None,
            allow_redirects=True,
    stream=False):
        header_dict = self.get_header_dict(header_string)
        work_obj = requests
        if sess is not None:
            work_obj = sess
        try:
            if proxy_ip is not None:
                proxies = {"http": "{}".format(
                    proxy_ip), "https": "{}".format(proxy_ip), }
                if json is not None:
                    rs = work_obj.post(
                        url,
                        json=json,
                        files=files,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        proxies=proxies,
                        params=params,
                        stream=stream,
                        allow_redirects=allow_redirects)
                else:
                    rs = work_obj.post(
                        url,
                        data=data,
                        files=files,
                        headers=header_dict,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        proxies=proxies,
                        params=params,
                        stream=stream,
                        allow_redirects=allow_redirects)
            else:
                if json is not None:
                    rs = work_obj.post(
                        url,
                        json=json,
                        headers=header_dict,
                        files=files,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        stream=stream,
                        params=params,
                        allow_redirects=allow_redirects)
                else:
                    rs = work_obj.post(
                        url,
                        data=data,
                        headers=header_dict,
                        files=files,
                        verify=SSL_verify,
                        cookies=cookie,
                        timeout=timeout,
                        stream=stream,
                        params=params,
                        allow_redirects=allow_redirects)
        except Exception as e:
            print(e)
            return None

        return rs

    def Put(
            self,
            url,
            data,
            header_string="",
            cookie="",
            SSL_verify=0,
            timeout=5,
            proxy_ip=None,
            params=None
    ):
        header_dict = self.get_header_dict(header_string)
        try:
            if proxy_ip is not None:
                proxies = {"http": "{}".format(
                    proxy_ip), "https": "{}".format(proxy_ip), }
                rs = requests.put(
                    url,
                    data=data,
                    headers=header_dict,
                    verify=SSL_verify,
                    cookies=cookie,
                    timeout=timeout,
                    proxies=proxies,
                    params=params)
            else:
                rs = requests.put(
                    url,
                    data=data,
                    headers=header_dict,
                    verify=SSL_verify,
                    cookies=cookie,
                    timeout=timeout,
                    params=params)
        except Exception as e:
            print(e)
            return None

        return rs
    # 將文字header變成字典

    def get_header_dict(self, string):
        string = string.replace("https://", "https#")
        string = string.replace("http://", "http#")
        arr = string.split("###")

        end = dict()
        for item in arr:
            if "Cookie" in item:
                pack = item.split('Cookie: ')
                end['Cookie'] = pack[1]
            else:
                if item != "":
                    temp = item.split(":")
                    if len(temp) < 2:
                        continue
                    temp[1] = temp[1].replace("https#", "https://")
                    temp[1] = temp[1].replace("http#", "http://")
                    end[temp[0].strip()] = temp[1].strip()
        return end

    # 用正則表達式取得文字
    def preg_get_word(self, preg_word, num, text, mode=0):
        try:
            patte = re.compile(preg_word)
            grk = patte.search(text)

            if num == "all":
                bb = re.findall(preg_word, text)
                rs = bb
                if len(rs) == 0:
                    rs = "empty_data"
            else:
                rs = grk.group(num)
                if mode == "test":
                    print("正則表達式:" + preg_word + "\n 結果:" + rs.encode("utf-8"))

        except BaseException:
            rs = "empty_data"

        return rs


if __name__ == "__main__":
    obj = Net()
    # 模擬測試
    header_str = "Host: class.ruten.com.tw###Connection: keep-alive###Cache-Control: max-age=0###Upgrade-Insecure-Requests: 1###User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36###Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8###Accept-Encoding: gzip, deflate###Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7###If-Modified-Since: Mon, 30 Jul 2018 19:28:15 GMT###"
    url = "http://class.ruten.com.tw/user/index00.php?s=dodo790119&d=5216722&o=0&m=1"
    rs = obj.Get(url, header_string=header_str)
    print(rs.content.decode())
    # print(rs)
