from urllib.request import urlopen
import bs4 as BeautifulSoup

html = urlopen('https://www.withhive.com/help').read()
soup = BeautifulSoup.BeautifulSoup(html, 'lxml')

for link in soup.find_all('a'):
    print(link.get('href'))
    print(link)