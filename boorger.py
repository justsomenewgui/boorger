#!/usr/bin/env python3

import argparse
from tools.startburger import Boorger

parser = argparse.ArgumentParser(description="""Downloads images and
videos from Gelbooru, Danbooru, Konachan and iibooru.""")
parser.add_argument("url", help="""Valid url. For example:
'https://gelbooru.com/index.php?page=post&s=list&tags=suigintou'""")
parser.add_argument("-d", "--directory", type=str,
                    default=None, help="""Directory to store
downloaded images. Must contain full path.
For example: '/home/user/Pictures/' If not given, images vill downloaded
to /booru_images/ in current working directory.""")
parser.add_argument("-p", "--pages", type=int, default=1, help="""
Number of pages you want to download.""")
parser.add_argument("-r", "--reverse", action="store_true", help="""
If selected, pages will be loaded in descending order.""")
args = parser.parse_args()
url = args.url
directory = args.directory
pages = args.pages
if args.reverse:
    reverse = True
else:
    reverse = False

#Start "startburger.py" from command line.
download = Boorger(url, directory, reverse)
download.loader(pages)
