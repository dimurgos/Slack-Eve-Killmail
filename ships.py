import util

ship_list = {}

def get_ship_by_id(id):
    if id in ship_list:
        return ship_list[id]
        
    root = util.get_public_esi_data('universe/types', id)
    
    typeName = root['name']
    ship_list[id] = typeName
    return typeName