from collections import defaultdict
from urlparse import urlparse
import urllib
from urllib2 import urlopen
from bs4 import BeautifulSoup


images = defaultdict(bool)


def get_flickr_pic(link, counter):
    global images  # sadface
    request = urlopen(link)
    soup = BeautifulSoup(request.read())
    imgs = soup.find_all('img')
    for img in imgs:
        if 'c1.staticflickr.com' in img['src'] and not images[img['src']]:
            images[img['src']] = True
            urllib.urlretrieve(img['src'], '../imgs/'+str(counter) + '.jpg')
            counter += 1
    return counter


with open('reddit_pics.txt', 'r') as f:
    links = f.readlines()
    links = [l.rstrip() for l in links]
    counter = 155 + 1
    for link in links:
        print link
        parsed_url = urlparse(link)
        if parsed_url.netloc == 'i.imgur.com':
            if not images[parsed_url.path]:
                images[parsed_url.path] = True
                urllib.urlretrieve(link, '../imgs/'+str(counter) + '.jpg')
                counter += 1
        elif parsed_url.netloc == 'imgur.com':

            link = link.split('/')[3]
            if not images["/" + link + ".jpg"]:
                images["/" + link + ".jpg"] = True
                link = 'http://i.imgur.com/' + link + '.jpg'
                urllib.urlretrieve(link, '../imgs/'+str(counter) + '.jpg')
                counter += 1
        elif parsed_url.netloc == 'www.flickr.com' or parsed_url.netloc == 'flic.kr':
            counter = get_flickr_pic(link, counter)
