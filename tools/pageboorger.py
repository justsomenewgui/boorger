import re
import sys

class PageBoorger:
    """Gives urls for next pages."""
    def __init__(self, url, reverse=False):
        self.url = url
        self.reverse = reverse

    def nextUrl(self):
        if 'gelbooru.com' in self.url:
            return self.glbtUrl()
        elif 'donmai.us' in self.url:
            return self.danbUrl()
        elif 'konachan.com' in self.url:
            return self.danbUrl()
        elif 'iibooru.org' in self.url:
            return self.danbUrl()
        elif 'chan.sankakucomplex.com' in self.url:
            return self.sankUrl()
        else:
            print('Wrong url for PageBoorger')
            sys.exit()

    def glbtUrl(self):
        if self.reverse is True:
            x = -42
        else:
            x = 42
        if 'pid=' in self.url:
            self.url = self.url.rsplit('=', 1)
            self.url[-1] = str(int(self.url[-1]) + x)
            if int(self.url[-1]) < 0:
                print('No more pages.')
                sys.exit()
            else:
                self.url = '='.join(self.url)
        else:
            if self.reverse is True:
                print('No more pages.')
                sys.exit()
            else:
                self.url = self.url + '&pid=42'
        return self.url

    def danbUrl(self):
        if self.reverse is True:
            x = -1
        else:
            x = 1
        if 'page=' in self.url:
            self.url = re.split('[=&]', self.url, 2)
            self.url[1] = str(int(self.url[1]) + x)
            if int(self.url[1]) <= 0:
                print('No more pages.')
                sys.exit()
            else:
                self.url = str(self.url[0] + '=' + self.url[1] + '&'
                               + self.url[2])
        else:
            if self.reverse is True:
                    print('No more pages.')
                    sys.exit()
            else:
                self.url = self.url.split('?')
                self.url = str(self.url[0] + '?page=2&' + self.url[1])
        return self.url

    def sankUrl(self):
        if self.reverse is True:
            x = -1
        else:
            x = 1
        if 'page=' in self.url:
            self.url = self.url.rsplit('=', 1)
            self.url[-1] = str(int(self.url[-1]) + x)
            if int(self.url[-1]) < 1:
                print('No more pages.')
                sys.exit()
            else:
                self.url = '='.join(self.url)
        else:
            if self.reverse is True:
                    print('No more pages.')
                    sys.exit()
            else:
                self.url = self.url + '&page=2'
        return self.url
