# Boorger. Downloads images and videos from Gelbooru, Danbooru, Konachan
# and iibooru.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

import sys
import argparse

# local import:
from boorger.startburger import Boorger

def main():
    """If user pass no arguments - return help message. Otherwise start
    the programm."""
    if len(sys.argv) > 1:
        start()
    else:
        sys.argv.append("--help")
        start()


def start():
    """https://docs.python.org/3/library/argparse.html"""
    
    parser = argparse.ArgumentParser(
        usage="""boorger url [optional arguments]""",
        description="""Downloads images and videos from Gelbooru, Danbooru,
        Konachan and iibooru.""")
    parser.add_argument(
        "url", nargs='?', help="""Valid url. For example:
        'https://gelbooru.com/index.php?page=post&s=list&tags=suigintou'""")
    parser.add_argument(
        "-d", "--directory", type=str, default=None,
        help="""Directory to store downloaded images. Must contain full path.
        For example: '/home/user/Pictures/' If not given, images vill
        downloaded to /booru_images/ in current working directory.""")
    parser.add_argument(
        "-p", "--pages", type=int, default=1,
        help="""Number of pages you want to download.""")
    parser.add_argument(
        "-r", "--reverse", action="store_true",
        help="""If selected, pages will be loaded in descending order.""")
    parser.add_argument(
        "-l", "--license", action="store_true",
        help="""Print the license of boorger.""")

    args = parser.parse_args()
    url = args.url
    directory = args.directory
    pages = args.pages
    if args.reverse:
        reverse = True
    else:
        reverse = False
    if args.license:
        gpl = __file__.rsplit("/", 1)[0] + "/LICENSE"
        with open(gpl) as f:
            my_license = f.read()
            print(my_license)
    elif not args.url:
        print("You need to pass valid url.")
    else:
        # Start "startburger.py" from command line.
        download = Boorger(url, directory, reverse)
        download.main(pages)
