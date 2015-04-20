###########################################################
############## Scraping reddit for pics ###################
###########################################################

import urllib2
import time
from bs4 import BeautifulSoup

subreddits = ['itookapicture', 'photocritique', 'HDR', 'photographs']
links = []

for sub in subreddits:
    for page in range(1, 6):
        # Sending request to reddit
        url = 'http://www.reddit.com/r/%s#page=%d' % (sub, page)
        print url

        # Handling a potential 429 error
        request = None
        while request is None:
            try:
                request = urllib2.urlopen(url)
            except(urllib2.HTTPError):
                time.sleep(1)
                pass

        html = ''
        data = request.read()
        for line in data:
            html += line
        soup = BeautifulSoup(html)

        # getting the links
        for link in soup.find_all('a'):
            try:
                if 'title' in link['class']:
                    links.append(str(link.attrs['href']))
                    print link
            except:
                continue

with open('reddit_pics.txt', 'w') as f:
    for link in links:
        f.write(link+"\n")

print "Done!"
