#!/usr/bin/env python
import urllib2
import urllib
import json
import sys
import exceptions
import locale
import config
import systems
import ships
from datetime import datetime
import time
import os
import signal

def run_killboard(config_type, config_id):
    kills = 'https://zkillboard.com/api/{0}/{1}/pastSeconds/{2}/'.format(config_type, config_id, config.config_check)

    locale.setlocale(locale.LC_ALL, config.config_locale)

    request = urllib2.Request(kills)
    request.add_header('User-Agent', config.config_header)
    opener = urllib2.build_opener()
    data = opener.open(request)
    root = json.load(data)

    handled_kills = []
    f = open('handled_kills.dat', 'r+')
    for line in f:
        handled_kills.append(line.rstrip('\n'))

    for record in root:
        try:
            kill_id = record['killID']
            if str(kill_id) in handled_kills:
                continue
            
            killers = []
            highestDealer = None
            killer = {}
            attackerCount = 0
            highestDmg = -1
            for attacker in record['attackers']:
                if attacker['finalBlow'] == 1:
                    killer = attacker
                if attacker['characterID'] == 0 and attacker['factionID'] != 0:
                    continue
                else:
                    attackerCount += 1
                if attacker['characterID'] != 0 and attacker['damageDone'] > highestDmg:
                    highestDmg = attacker['damageDone']
                    highestDealer = attacker
                if config.config_show_participating and attacker[config_type] == config_id:
                	killers.append({'characterName': attacker['characterName'], 'characterID': attacker['characterID'], 'corporationName': attacker['corporationName'], 'corporationID': attacker['corporationID'], 'damageDone': attacker['damageDone']})

            victim = record['victim']

            attachment = {}
            damageTaken = {}
            kill = {}
            
            if killer['characterID'] == 0:
                killerName = killer['shipTypeID']
            else:
                killerName = killer['characterName']
            if victim['characterID'] == 0:
                victimName = victim['shipTypeID']
            else:
                victimName = victim['characterName']
            
            if victim[config_type] == config_id:
            	if config.config_extended_name: 
            		if killer['allianceName'] == '':
            			allianceName = ''
            		else:
            			allianceName = ' ({0})'.format(killer['allianceName'])
                	kill['fallback'] = '{0} ({1}) got killed by {2} ({3}){4}'.format(victimName, victim['corporationName'], killerName, killer['corporationName'], allianceName)
                else:
                	kill['fallback'] = '{0} got killed by {1} ({2})'.format(victimName, killerName, killer['corporationName'])
                kill['color'] = 'danger'
                damageTaken['title'] = "Damage taken"
            else:
            	if config.config_extended_name: 
            		if victim['allianceName'] == '':
            			allianceName = ''
            		else:
            			allianceName = ' ({0})'.format(victim['allianceName'])
                	kill['fallback'] = '{0} ({1}) killed {2} ({3}){4}'.format(killerName, killer['corporationName'], victimName, victim['corporationName'], allianceName)
                else:
                	kill['fallback'] = '{0} killed {1} ({2})'.format(killerName, victimName, victim['corporationName'])
                kill['color'] = 'good'
                damageTaken['title'] = "Damage dealt"

            kill['title'] = kill['fallback']
            kill['title_link'] = 'https://zkillboard.com/kill/{0}/'.format(kill_id)
            kill['thumb_url'] = 'https://imageserver.eveonline.com/Render/{0}_64.png'.format(victim['shipTypeID'])
            
            damageTaken['value'] = locale.format('%d', victim['damageTaken'], grouping=True)
            damageTaken['short'] = "true"
            
            value = {'title': 'Value', 'value': locale.format('%d', record['zkb']['totalValue'], grouping=True) + ' ISK', 'short': False}
            totalAttackers = {'title': 'Pilots involved', 'value': str(attackerCount), 'short': 'true'}

            mostDmg = {}
            if highestDealer and highestDealer['characterID'] != 0:
                mostDmg['title'] = 'Most Damage'
                mostDmg['value'] = '<https://zkillboard.com/character/{0}|{1}> ({2})'.format(highestDealer['characterID'], highestDealer['characterName'], locale.format('%d', highestDmg, grouping=True))
                mostDmg['short'] = "true"
            
            solarSystemName,regionID,regionName,constellationName,security = systems.get_system_by_id(record['solarSystemID'])
            system = {'title': 'System', 'value': '<https://zkillboard.com/system/{systemID}|{systemName}> ({security:.1g}) / <https://zkillboard.com/region/{regionID}|{regionName}> / {constellationName}'.format(
                systemID = record['solarSystemID'], 
                systemName = solarSystemName, 
                security = security,
                regionName = regionName,
                regionID = regionID,
                constellationName = constellationName
            ), 'short': False}
            ship = {'title': 'Ship', 'value': '{0}'.format(ships.get_ship_by_id(victim['shipTypeID'])), 'short': 'true'}
            
            if config.config_show_participating:
            	row_damage = {'fallback': kill['fallback'], 'color': kill['color'], 'title': kill['title'], 'title_link': kill['title_link'], 'fields': [damageTaken, totalAttackers], 'thumb_url': 'https://imageserver.eveonline.com/Corporation/{0}_64.png'.format(victim['corporationID'])}
            	row_ship = {'color': kill['color'], 'fields': [mostDmg, ship], 'thumb_url': kill['thumb_url']}
            	row_value = {'color': kill['color'], 'fields': [value]}
            	row_system = {'color': kill['color'], 'fields': [system]}
            	attachment['attachments'] = [row_damage, row_ship, row_value, row_system]
            	i = 0
            	for attacker in killers:
            		attacker_name = {'title': 'Attacker', 'value': '<https://zkillboard.com/character/{0}|{1}> ({2})'.format(attacker['characterID'], attacker['characterName'], attacker['corporationName']), 'short': 'true'}
            		attacker_damage = {'title': 'Damage Done', 'value': locale.format('%d', attacker['damageDone'], grouping=True), 'short': 'true'}
            		attachment['attachments'].append({'color': kill['color'], 'fields': [attacker_name, attacker_damage], 'thumb_url': 'https://imageserver.eveonline.com/Corporation/{0}_64.png'.format(attacker['corporationID'])})
            		i += 1
            		if i == 10:
            			break
            else:
            	kill['fields'] = [damageTaken, totalAttackers, mostDmg, ship, value, system]
            	attachment['attachments'] = [kill]
            
            payload = json.dumps(attachment)
            
            data = urllib.urlencode({'payload': payload})
            
            request_slack = urllib2.Request(config.config_slack_url, data)
            urllib2.urlopen(request_slack)

            time.sleep(2)
            f.write('{0}\n'.format(kill_id))
        except urllib2.HTTPError as e:
            print "HTTPError in processing record: " + str(e.reason)
        except exceptions.KeyError as e:
            print "KeyError in processing record: " + str(e)
        except exceptions.NameError as e:
            print "NameError in processing record: " + str(e)
        except Exception:
            print "Generic Exception in processing record: " + str(sys.exc_info()[0]) + " (" + str(sys.exc_info()[1]) + ")"
        
    f.close()
    
def make_pid():
    try:
        os.stat('/var/run')
    except:
        os.mkdir('/var/run')
    f = open('/var/run/kbbot.pid', 'w+')
    f.truncate()
    f.write(str(os.getpid()))
    f.write("\n");
    f.close()

def signal_handler(signal, frame):
    os.remove('/var/run/kbbot.pid')
    exit()

if config.config_run_as_daemon:
	make_pid()
	signal.signal(signal.SIGINT, signal_handler)

while True:
    try:
        for group in config.config_owner:
            for key,val in group.items():
                run_killboard(key, val)
            time.sleep(60)
        time.sleep(config.config_sleep_time)
    except urllib2.HTTPError as e:
        print "HTTPError in processing killboard data: " + str(e.reason)
        time.sleep(60)
    except Exception:
        print "Exception in processing killboard data: " + str(sys.exc_info()[0]) + " (" + str(sys.exc_info()[1]) + ")"
        time.sleep(60)
