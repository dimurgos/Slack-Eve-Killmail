import urllib2
import urllib
import json
import config

def get_public_crest_data(type, id):
    request = urllib2.Request('https://public-crest.eveonline.com/{0}/{1}/'.format(type, id))
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    data = opener.open(request)
    return json.load(data)
    
def get_public_crest_data_href(href):
    request = urllib2.Request(href)
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    data = opener.open(request)
    return json.load(data)
