import sqlite3

def get_system_by_id(id):
    conn = sqlite3.connect('universeDataDx.db')
    cursor = conn.cursor()
    cursor.execute('SELECT mapSolarSystems.solarSystemName, mapRegions.regionID, mapRegions.regionName, mapConstellations.constellationName, mapSolarSystems.security FROM mapSolarSystems INNER JOIN mapConstellations ON mapConstellations.constellationID = mapSolarSystems.constellationID INNER JOIN mapRegions ON mapRegions.regionID = mapSolarSystems.regionID WHERE solarSystemID = ?', (str(id),));
    result = cursor.fetchone()
    conn.close()
    return result
#conn = sqlite3.connect('universeDataDx.db')
#cursor = conn.cursor()
#cursor.execute('SELECT mapSolarSystems.solarSystemName, mapRegions.regionID, mapRegions.regionName, mapConstellations.constellationName, mapSolarSystems.security FROM mapSolarSystems INNER JOIN mapConstellations ON mapConstellations.constellationID = mapSolarSystems.constellationID INNER JOIN mapRegions ON mapRegions.regionID = mapSolarSystems.regionID WHERE solarSystemID = ?', (str(30003855),));
#result = cursor.fetchone()
#print result
#conn.close()

#SELECT mapSolarSystems.solarSystemName, mapRegions.regionName, mapConstellations.constellationName, mapSolarSystems.security FROM mapSolarSystems INNER JOIN mapConstellations ON mapConstellations.constellationID = mapSolarSystems.constellationID INNER JOIN mapRegions ON mapRegions.regionID = mapSolarSystems.regionID WHERE solarSystemID = ?