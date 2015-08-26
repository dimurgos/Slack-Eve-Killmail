import sqlite3

def get_system_by_id(id):
    conn = sqlite3.connect('universeDataDx.db')
    cursor = conn.cursor()
    cursor.execute('SELECT solarSystemName, security FROM mapSolarSystems WHERE solarSystemID = ?', (str(id),));
    result = cursor.fetchone()
    conn.close()
    return result
