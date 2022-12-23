from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    """To better understand what's happening here, go to:
    https://docs.python.org/3/library/html.parser.html
    """
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = set()  # Accumulating links from parser
        self.img = set()     # Accumulating links to images
        
    def starter(self, data):
        """Returning set of links from parser."""
        MyHTMLParser.feed(self, data)
        return self.result
    
    def imager(self, data):
        """Returning set of links to images from parser."""
        MyHTMLParser.feed(self, data)
        return self.img
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    # gelbooru and safebooru.org section:
                    if 's=view' in value:
                        if 'https://' in value:
                            self.result.add(value)
                        else:
                            value = 'https://safebooru.org/' + value
                            self.result.add(value)
                    # Also maching safebooru
                    elif '//images/' in value:
                        self.img.add(value)
                    elif 'gelbooru.com/images/' in value:
                        self.img.add(value)
                    # danbooru section:
                    elif '/posts/' in value and '/random' not in value:
                        value = 'https://danbooru.donmai.us' + value
                        self.result.add(value)
                    elif 'donmai.us/original/' in value:
                        value = value.split('?')
                        value = value[0]
                        self.img.add(value)
                    # konachan section:
                    elif 'https://konachan.com/' in value:
                        self.img.add(value)
                    # iibooru section:
                    elif '/data/image/' in value:
                        value = 'https://iibooru.org/' + value
                        self.img.add(value)
                    # sankaku section:
                    elif '/post/show/' in value:
                        value = 'https://chan.sankakucomplex.com' + value
                        self.result.add(value)
                    elif 's.sankakucomplex.com/data/' in value:
                        if '/sample/' not in value:
                            value = 'https:' + value
                            self.img.add(value)
