from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    """To better understand what's happening here, go to:
    https://docs.python.org/3.9/library/html.parser.html
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = set() #Accumulating links from parser
        self.img = set()    #Accumulating links to images
        
    def starter(self, data):
        MyHTMLParser.feed(self, data)
        return self.result
    def imager(self, data):
        MyHTMLParser.feed(self, data)
        return self.img
        
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    #gelbooru section:
                    if 'view&id=' in value:
                        self.result.add(value)
                    elif 'gelbooru.com//images/' in value:
                        self.img.add(value)
                    elif 'gelbooru.com/images/' in value:
                        self.img.add(value)
                    #danbooru section:
                    elif '/posts/' in value and '/random' not in value:
                        value = 'https://danbooru.donmai.us' + value
                        self.result.add(value)
                    elif 'donmai.us/original/' in value:
                        value = value.split('?')
                        value = value[0]
                        self.img.add(value)
                    #konachan section:
                    elif 'https://konachan.com/' in value:
                        self.img.add(value)
                    #iibooru section:
                    elif '/data/image/' in value:
                        value = 'https://iibooru.org/' + value
                        self.img.add(value)
                    
