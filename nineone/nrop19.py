#!/usr/bin/env python2
# vim: set fileencoding=utf8

import sys
import requests
import urlparse
import re
import urllib2
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"q=0.8,zh-CN;en-US,en;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 " \
        "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
}

ss = requests.session()
ss.headers.update(headers)

class nrop19(object):
    def get_video_url(self, url):
        resp = ss.get(url)
        if resp.ok:
            n1 = re.search(r'so.addVariable\(\'file\',\'(\d+)\'', resp.content)
            n2 = re.search(r'so.addVariable\(\'seccode\',\'(.+?)\'', resp.content)
            n3 = re.search(r'so.addVariable\(\'max_vid\',\'(\d+)\'', resp.content)

            if n1 and n2 and n3:
                apiurl = 'http://%s/getfile.php' \
                    % urlparse.urlparse(url).hostname
                logger.debug("apiurl: %s", apiurl)

                params = {
                    'VID': n1.group(1),
                    'mp4': '0',
                    'seccode': n2.group(1),
                    'max_vid': n3.group(1),
                }
                logger.debug("params: %s", params)

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
                raise Exception("get url %s failed", url)

    def download_video(self, url, file_path):
        resp = ss.get(url, stream=True)
        total_downloaded = 0
        flush = 64
        logger.info('start to download %s to %s', (url, file_path))
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


