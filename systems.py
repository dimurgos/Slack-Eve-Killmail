import util

region_list = {}

def get_system_by_id(id):
    if id in region_list:
        return region_list[id]

    solarsystem = util.get_public_esi_data('universe/systems', id)
    constellation = util.get_public_esi_data('universe/constellations', solarsystem['constellation_id'])
    region = util.get_public_esi_data('universe/regions', constellation['region_id'])
    
    region_info = (solarsystem['name'], int(constellation['region_id']), region['name'], constellation['name'], solarsystem['security_status'])
    region_list[id] = region_info
    return region_info
