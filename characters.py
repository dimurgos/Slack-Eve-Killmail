import util

character_list = {}

def get_character_by_id(id):
    if id in character_list:
        return character_list[id]

    root = util.get_public_esi_data('characters', id)

    name = root['name']
    character_list[id] = name
    return name