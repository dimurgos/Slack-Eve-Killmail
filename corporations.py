import util

corporation_list = {}

def get_corporation_by_id(id):
    if id in corporation_list:
        return corporation_list[id]
        
    root = util.get_public_esi_data('corporations', id)
    
    name = root['name']
    corporation_list[id] = name
    return name
