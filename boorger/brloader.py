import os
import urllib.request


def loader(link, agent, cookie):
    """For more info visit:
    https://docs.python.org/3/library/urllib.request.html
    """
    print('Download url:', link)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', agent), ('Cookie', cookie)]
    with opener.open(link) as remotefile:
        remotedata = remotefile.read().decode('utf-8')
        return remotedata


def imgloader(link, agent, cookie, directory):
    """Just saves files from given link."""
    filenames = os.listdir(directory)
    image_name = os.path.basename(link)
    if 'sankakucomplex.com' in link:
        image_name = image_name.split('?')
        image_name = image_name[0]
    if image_name in filenames:
        print(image_name, 'Image already downloaded')
    else:
        print('Download image:', link)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', agent), ('Cookie', cookie)]
        with opener.open(link) as remoteimg:
            image_name = directory + image_name
            image = remoteimg.read()
            with open(image_name, 'wb') as myimage:
                myimage.write(image)
