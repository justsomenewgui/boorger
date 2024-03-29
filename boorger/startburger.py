import os
import sys
from threading import Thread

# local import:
from boorger import brloader
from boorger.pageboorger import PageBoorger
from boorger.parsboorger import MyHTMLParser


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
            'iibooru.org',
            'safebooru.org',
            'chan.sankakucomplex.com'
            )
        #Check is url in supported, or not.
        check = self.url.replace('www.', '').split('/')
        if check[2] not in supported:
            print('Unsupported url')
            sys.exit()
        self.result = set()  # Container for links from parser.

    def main(self, pages=1):
        link = self.url
        remotedata = brloader.loader(link, self.agent, self.cookie)
        parser = MyHTMLParser()
        #Line below is sites, that need one more step to parsing files
        two_step_pars = ('gelbooru.com',
                         'danbooru.donmai.us',
                         'safebooru.org')
        check = link.replace('www.', '').split('/')
        if check[2] in two_step_pars:
            links = list(parser.starter(remotedata))
            if len(links) == 0:
                print('parser.starter give no links')
                sys.exit()
            # Downloading html pages:
            self.loader(links, target=Boorger.thr_loader)
            links = list(self.result)
        elif 'chan.sankakucomplex.com' in self.url:
            # sankaku asking to slow down. So we downloading it slow.
            links = list(parser.starter(remotedata))
            for link in links:
                self.thr_loader(link)
            links = list(self.result)
        else:
            # Here go links for sites, that dont need first step.
            links = list(parser.imager(remotedata))
        if len(links) == 0:
            print('parser.imager give no links')
            sys.exit()
        if 'chan.sankakucomplex.com' in self.url:
            # sankaku asking to slow down. So we downloading it slow.
            for link in links:
                brloader.imgloader(link, self.agent, self.cookie,
                                   self.directory)
        else:
            # Downloading files:
            self.loader(links, target=Boorger.img_loader)

        self.result.clear()  # reset olg results
                
        nextpage = PageBoorger(self.url, self.reverse)
        while pages > 1:
            print('Browse next page')
            self.url = nextpage.nextUrl()
            self.main()
            pages = pages - 1

    def loader(self, links, target):
        """Downloading html pages or files with threading.Thread and
        
        pars links to images from them with html.parser.HTMLParser
        https://docs.python.org/3/library/threading.html
        """
        start = 0  # Breaking a list of links into pieces,
        end = 20   # to avoid too long list.
        while True:
            try:
                threads = []
                for x in range(start, end):
                    thread = Thread(target=target, args=(self, links[x]))
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
        
    def thr_loader(self, link):
        """Function for loading links with threading.Thread
        https://docs.python.org/3/library/threading.html
        """
        data = brloader.loader(link, self.agent, self.cookie)
        myparser = MyHTMLParser()
        links = myparser.imager(data)
        self.result.update(links)

    def img_loader(self, link):
        brloader.imgloader(link, self.agent, self.cookie, self.directory)
