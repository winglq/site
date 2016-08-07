from bs4 import BeautifulSoup
import requests
import eventlet
import re

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 " \
        "(KHTML, like Gecko) Chrome/32.0.1700.77 Safari/537.36"
}
ss = requests.session()
ss.headers.update(headers)
resp = ss.get("http://sh.k7p.work/v.php?category=tf&viewtype=basic")
soup = BeautifulSoup(resp.text, 'html.parser')
for x in soup.find_all('div', 'listchannel'):
    print x.find('a', recursive=False).get('title')
    print x.find('a', recursive=False).get('href')
    text = x.get_text()
    m = re.search('Favorites:\s(\d+)\s', text)
    if m:
        print m.group(1)
