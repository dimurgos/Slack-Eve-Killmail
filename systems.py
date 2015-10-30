import util

region_list = {}

def get_system_by_id(id):
    if id in region_list:
        return region_list[id]

    solarsystem = util.get_public_crest_data('solarsystems', id)
    constellation = util.get_public_crest_data_href('constellations', solarsystem['constellation']['href'])
    region = util.get_public_crest_data_href('regions', constellation['region']['href'])
    
    region_info = (solarsystem['name'], int(constellation['region']['href'].split('/')[4]), region['name'], constellation['name'], solarsystem['securityStatus'])
    region_list[id] = region_info
    return region_info
