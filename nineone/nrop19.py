#!/usr/bin/env python2
# vim: set fileencoding=utf8

import sys
import requests
import urlparse
import re
import urllib2
import logging
from bs4 import BeautifulSoup
import subprocess


logger = logging.getLogger(__name__)

headers = {
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;zh-CN, zh; q=0.8",
    "Accept":"*/*",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Connection": "keep-alive",
}

ss = requests.session()
ss.headers.update(headers)

class nrop19(object):
    def get_resp_by_wget(self, url):
        cmd = 'wget -c -O "%s"  "%s"' \
            % ('/tmp/tmp.html', url)
        subprocess.check_call(cmd, shell=True)
        with open('/tmp/tmp.html', 'r') as f:
            cnt = f.read()
        class resp(object):
            def __init__(self, cnt):
                self.content=cnt
                self.ok = True
        return resp(cnt)

    def get_video_url(self, url):
        resp = ss.get(url)
        #resp = self.get_resp_by_wget(url)
        if resp.ok:
            n1 = re.search(r'so.addVariable\(\'file\',\'(\d+)\'', resp.content)
            n2 = re.search(r'so.addVariable\(\'seccode\',\'(.+?)\'', resp.content)
            n3 = re.search(r'so.addVariable\(\'max_vid\',\'(\d+)\'', resp.content)

            if n1 and n2 and n3:
                apiurl = 'http://%s/getfile.php' \
                    % urlparse.urlparse(url).hostname
                logger.info("apiurl: %s", apiurl)

                params = {
                    'VID': n1.group(1),
                    'mp4': '0',
                    'seccode': n2.group(1),
                    'max_vid': n3.group(1),
                }
                logger.debug("params: %s", params)
                ss.headers.update({"Referer": url, "X-Requested-With": "ShockwaveFlash/24.0.0.194"})
                import eventlet
                eventlet.sleep(20)
                logging.debug(ss.cookies)
                logging.debug(ss.headers)

                resp = ss.get(apiurl, params=params)
                if resp.ok:
                    dlink = re.search(
                        r'file=(http.+?)&', resp.content).group(1)
                    dlink = urllib2.unquote(dlink)
                    logger.debug("dlink: %s", dlink)
                    return dlink
                else:
                    raise Exception("get api url fail")
            else:
                raise Exception("pattern not found at %s" % url)
        else:
            raise Exception("get url %s failed" % url)

    def download_video(self, url, file_path):
        resp = ss.get(url, stream=True)
        total_downloaded = 0
        flush = 64
        logger.info('start to download %s to %s', url, file_path)
        with open(file_path, 'w') as f:
            for chunk in resp.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
                    total_downloaded +=4
                    flush -= 1
                    sys.stdout.write("%sk of file is downloaded \r" % (total_downloaded))
                    if not flush:
                        sys.stdout.flush()
                        flush = 64
        logger.info("%s download completed", file_path)

    def download_video2(self, url, file_path):
        logger.info('start to download %s to %s', url, file_path)
        cookies = '; '.join(
            ['%s=%s' % (i, ii) for i, ii in ss.cookies.items()])

        cmd = 'wget -c -O "%s" --header "User-Agent: %s" ' \
            '--header "Cookie: %s" "%s"' \
            % (file_path, headers['User-Agent'], cookies, url)

        subprocess.check_call(cmd, shell=True)
        logger.info("%s download completed", file_path)


    def get_all_video_info_from_url(self, url):
        resp = ss.get(url)
        if not resp.ok:
            raise Exception("get url %s failed", url)

        soup = BeautifulSoup(resp.text, 'html.parser')
        infos = []
        for x in soup.find_all('div', 'listchannel'):

            text = x.get_text()
            m = re.search('Favorites:\s(\d+)\s', text)
            if m:
                fav = m.group(1)
                if int(fav) > 2000:

                    info = {}
                    info['title'] = x.find('a', recursive=False).get('title')
                    info['href'] = x.find('a', recursive=False).get('href')
                    infos.append(info)
                    logger.debug("new video info %s", info)
        return infos


if __name__ == "__main__":
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    none = nrop19()
    print none.get_video_url("http://68.235.35.99/view_video.php?viewkey=0bbb1e9ebc00f06ae397&page=1&viewtype=basic&category=tf")

