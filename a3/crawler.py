# -------------------------------------------------------------------------
# AUTHOR: Francisco Serrano
# FILENAME: crawler.py
# SPECIFICATION: Use seed url and crawl through the pages until you hit the target page
# FOR: CS 4250 - Assignment 3
# TIME SPENT: 2hrs
# -----------------------------------------------------------*/
from collections import deque
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient


def main():
    frontier = WebCrawlerFrontier()
    seed_urls = ['https://www.cpp.edu/sci/computer-science/']
    for url in seed_urls:
        frontier.add_url(url=url.strip())
    crawlerThread(frontier=frontier)


class WebCrawlerFrontier:
    def __init__(self):
        # for managing which we visited/processed the webpage of
        self.visited = set()
        # for managing retrieval
        self.frontier = deque()
        # for fast look up
        self.frontier_set = set()

    def add_url(self, url: str):
        if url not in self.visited and url not in self.frontier_set:
            # for now just store the url,
            # might want to store something more important later
            self.frontier.append(url)
            self.frontier_set.add(url)

    def processed_url(self, url: str):
        if url not in self.visited:
            self.visited.add(url)

    def get_next_url(self):
        # frontier exits and it is non empty
        if self.frontier:
            url = self.frontier.popleft()
            self.frontier_set.remove(url)
            return url
        else:
            print("is it empty")
            return None

    def is_done(self):
        if not self.frontier or self.frontier is None:
            return True
        else:
            return False

    def clear(self):
        self.visited = None
        self.frontier = None
        self.frontier_set = None


def crawlerThread(frontier: WebCrawlerFrontier):

    while not frontier.is_done():
        url = frontier.get_next_url()
        # print("This is the frontier now:")
        # print(frontier.frontier)
        if (url):
            try:
                html = urlopen(url)
                html_content = html.read().decode('utf-8')
                storePage(url=url, html=html_content)
                # storePage(url=url, html=html.read().decode('utf-8'))
                soup = BeautifulSoup(html_content, 'html.parser')
                if (target_page(soup)):
                    print("we hit the target page")
                    print(url)
                    frontier.clear()
                else:
                    # get urls from the soup
                    extracted_urls = extract_urls(soup, url)
                    for url in extracted_urls:
                        # my add_url method has the logic that checks
                        # if it was visited or not
                        frontier.add_url(url=url)
            except HTTPError as e:
                print(e)
            except URLError:
                print('The server could not be found!')
            except Exception as e:
                print("Unexpected error:", e)


def storePage(html, url):
    # pymongo related stuff
    try:
        client = MongoClient('mongodb://localhost:27017/')
        pages_collection = client['corpus']['pages']
        page = {'_id': url, 'html': html}
        pages_collection.insert_one(page)
        pass
    except Exception:
        print("not able to connect to db")


def target_page(soup: BeautifulSoup):
    # Stop criteria: when the crawler finds the "Permanent Faculty"
    #  heading on the page body.
    headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    regex = re.compile("Permanent Faculty")
    num_of_hits = len(soup.find_all(headings, string=regex))
    return num_of_hits == 1


def extract_urls(soup: BeautifulSoup, linker_url: str):
    # find all the urls, note:
    # Links might appear with full or relative addresses,
    #  and your crawler needs to consider this.
    urls = []
    try:
        regex = re.compile(".html")
        url_tags = soup.find_all("a", {'href': regex})
        for url_tag in url_tags:
            url = str(url_tag.attrs.get('href'))
            full_url = urljoin(linker_url, url)
            urls.append(full_url)
    except Exception as e:
        print("Error extracting URLs:", e)
    return urls


if __name__ == '__main__':
    main()

# logic i was planning because i thought we had to resolve them on our own
# to check for relative or full addresses
# url_components = url.split("://")
# num_of_components = len(url_components)
# is a relative url
# if num_of_components == 1:
#     # pretty sure we can use urljoin since he says we can use urlib
#     # and this is a utility function in a submodule -- scrap this
#     # case 1: root relative (begins with /)
#     # take str (https?) + (hostname) + / + root relative string
#     # check if it starts with a /
#     # if url.startswith("/"):
#     #     full_url = linker_url + url
#     #     print("For the root relative link we found,
#               here is the full url", full_url)
#     #     urls.append(full_url)
#     # case 2: relative to some parent directory:
#     # ex: ../page2.html , ../folder/page2.html, ../../../page2.html
#     # elif url.startswith("../"):
#     #     url_components = url.split("/")
#     #     linked_components =
#     #     for component in url_components:
#     # case 3: relative to current doc/page (explicit)
#     # ex :  ./page2.html or ./folder/page2.html
#     # case 4 : relative to current doc or page (implicit)
#     # ex : page2.html, folder/page2.html
# elif num_of_components == 2:
#     # is a full address, can add it directly
#     urls.append(url)
#     pass
