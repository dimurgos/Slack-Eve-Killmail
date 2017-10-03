import urllib2
import urllib
import json
import config

def get_public_esi_data(type, id):
    request = urllib2.Request('https://esi.tech.ccp.is/latest/{0}/{1}/'.format(type, id))
    request.add_header('X-User-Agent', config.config_header)
    request.add_header('Accept', 'application/json;charset=utf-8')
    opener = urllib2.build_opener()
    data = opener.open(request)
    return json.load(data)

