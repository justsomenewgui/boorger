import os
import sys
from threading import Thread

# local import:
from tools import brloader
from tools.pageboorger import PageBoorger
from tools.parsboorger import MyHTMLParser


class Boorger:
    """Downloads images and videos from Gelbooru, Danbooru,
    Konachan and iibooru."""
    
    def __init__(self, url, directory=None, reverse=False):
        self.url = url
        self.directory = directory
        if self.directory == None:
            # If directory does not given by user, creating /booru_images/
            # in current working directory.
            self.directory = os.getcwd() + '/booru_images/'
            try:
                os.makedirs(self.directory)
            except FileExistsError:
                pass
        else:
            try:
                os.makedirs(self.directory)
            except FileExistsError:
                pass
        self.reverse = reverse
        self.agent = ("Mozilla/5.0 (X11; Linux x86_64; rv:96.0) "
                      + "Gecko/20100101 Firefox/96.0")
        if 'gelbooru.com' in self.url:
            # Enable to load all categories
            self.cookie = 'fringeBenefits=yup'
        else:
            self.cookie = ''
        supported = (
            'gelbooru.com',
            'danbooru.donmai.us',
            'konachan.com',
            'iibooru.org'
            )
        #Check is url in supported, or not.
        check = self.url.replace('www.', '')
        check = check.split('/')
        if check[2] not in supported:
            print('Unsupported url')
            sys.exit()
        self.result = set()  # Container for links from parser.

    def main(self, pages=1):
        link = self.url
        remotedata = brloader.loader(link, self.agent, self.cookie)
        parser = MyHTMLParser()
        #Line below is sites, that need one more step to parsing files
        two_step_pars = ('gelbooru.com', 'danbooru.donmai.us')
        check = link.replace('www.', '')
        check = check.split('/')
        if check[2] in two_step_pars:
            links = parser.starter(remotedata)
            links = list(links)
            if len(links) == 0:
                print('parser.starter give no links')
                sys.exit()
            # Downloading html pages with threading.Thread
            # and pars links to images from them with html.parser.HTMLParser
            # https://docs.python.org/3/library/threading.html
            start = 0  # Breaking a list of links into pieces,
            end = 20   # to avoid too long list.
            while True:
                try:
                    threads = []
                    for x in range(start, end):
                        thread = Thread(
                            target=Boorger.thr_loader,
                            args=(self, links[x], self.agent, self.cookie))
                        thread.start()
                        threads.append(thread)
                    for thread in threads:
                        thread.join()
                    start = end
                    end = end + 20
                except IndexError:
                    for thread in threads:
                        thread.join()
                    break
            links = list(self.result)
        else:
            # Here go links for sites, that dont need first step.
            links = parser.imager(remotedata)
            links = list(links)
        if len(links) == 0:
            print('parser.imager give no links')
            sys.exit()
        start = 0
        end = 20
        while True:
            try:
                threads = []
                for x in range(start, end):
                    thread = Thread(
                        target=brloader.imgloader,
                        args=(links[x], self.directory, self.agent,
                              self.cookie))
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    thread.join()
                start = end
                end = end + 20
            except IndexError:
                for thread in threads:
                    thread.join()
                break
                
        self.result.clear()  # reset old results
        nextpage = PageBoorger(self.url, self.reverse)
        while pages > 1:
            print('Browse next page')
            self.url = nextpage.nextUrl()
            Boorger.main(self)
            pages = pages - 1
        
    def thr_loader(self, link, agent, cookie):
        """Function for loading links with threading.Thread
        https://docs.python.org/3/library/threading.html
        """
        data = brloader.loader(link, agent, cookie)
        myparser = MyHTMLParser()
        links = myparser.imager(data)
        self.result = self.result.union(links)
