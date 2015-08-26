import xml.etree.ElementTree as ET
import urllib2
import urllib
import config

ship_list = {}

def get_ship_by_id(id):
    if id in ship_list:
        return ship_list[id]

    request = urllib2.Request('https://api.eveonline.com/eve/TypeName.xml.aspx?ids={0}'.format(id))
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    root = ET.parse(opener.open(request))

    for record in root.findall('./result/rowset/row'):
        typeName = record.get('typeName')
        ship_list[id] = typeName
        return typeName