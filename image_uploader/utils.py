import mimetypes
import httplib
import urllib2
import os
import StringIO
import magic
from urlparse import urlparse
from django.core.files.base import ContentFile


MAX_SIZE = 4*1024*1024
VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]
VALID_IMAGE_MIMETYPES = [
    "image"
]


def split_url(url):
    parse_object = urlparse(url)
    return parse_object.netloc, parse_object.path

def get_url_tail(url):
    return url.split('/')[-1]

def get_extension(filename):
    return os.path.splitext(filename)[1]

def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    '''
    A simple method to make sure the URL the user has supplied has
    an image-like file at the tail of the path
    '''
    return any([url.endswith(e) for e in extension_list])


def get_mimetype(fobject):
    '''
    Guess mimetype of a file using python-magic
    '''
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobject.read(1024))
    fobject.seek(0)
    return mimetype


def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    '''
    As an alternative to checking the url extension, a basic method to
    check the image file in the URL the user has supplied has an
    image mimetype

    - https://docs.python.org/2/library/mimetypes.html
    '''
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(m) for m in mimetype_list])
    else:
        return False


def valid_image_mimetype(fobject):
    '''
    Look inside the file using python-magic to make sure the mimetype
    is an image

    - http://stackoverflow.com/q/20272579/396300
    '''
    mimetype = get_mimetype(fobject)
    if mimetype:
        return mimetype.startswith('image')
    else:
        return False

def image_exists(domain, path, check_size=False, size_limit=1024):
    '''
    Make a HEAD request to the remote server to make sure the image
    actually exists before downloading. Also, check the headers sent
    back to check the image size

    - http://stackoverflow.com/q/5616102/396300
    '''
    try:
        conn = httplib.HTTPConnection(domain)
        conn.request('HEAD', path)
        response = conn.getresponse()
        headers = response.getheaders()
        conn.close()
    except:
        return False

    try:
        length = int([x[1] for x in headers if x[0] == 'content-length'][0])
    except:
        length = 0
    if length > MAX_SIZE:
        return False

    return response.status == 200


def retrieve_image(url):
    '''Download the image from the remote server'''
    return StringIO.StringIO(urllib2.urlopen(url).read())

def valid_image_size(image, max_size=MAX_SIZE):
    width, height = image.size
    if (width * height) > max_size:
        return (False, "Image is too large")
    return (True, image)

def pil_to_django(image, format="JPEG"):
    '''http://stackoverflow.com/questions/3723220/how-do-you-convert-a-pil-image-to-a-django-file'''
    fobject = StringIO.StringIO()
    image.save(fobject, format=format)
    return ContentFile(fobject.getvalue())