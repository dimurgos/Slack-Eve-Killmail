import util

alliance_list = {}

def get_alliance_by_id(id):
    if id in alliance_list:
        return alliance_list[id]
        
    root = util.get_public_esi_data('alliances', id)
    
    name = root['alliance_name']
    alliance_list[id] = name
    return name