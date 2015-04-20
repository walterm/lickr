from urlparse import urlparse
import urllib

def get_imgur_pic(parsed_url):
    pass

with open('reddit_pics.txt', 'r') as f:
    links = f.readlines()
    links = [l.rstrip() for l in links]
    counter = 0
    for link in links:
        parsed_url = urlparse(link)
        if parsed_url.netloc == 'i.imgur.com':
            print link
            urllib.urlretrieve(link, './imgs/'+str(counter) + '.jpg')
            counter += 1